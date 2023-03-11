from pathlib import Path
from typing import Any, Union

import pandas as pd
from dagster import Field, InputContext, IOManager, OutputContext
from dagster import _check as check
from dagster import io_manager
from dagster._seven.temp_dir import get_system_temp_directory

from .utils import get_output_metadata_entries


class PartitionedParquetIOManager(IOManager):
    """
    This IOManager will take in a Pandas DataFrame and store it in parquet at the
    specified path.

    It stores outputs for different partitions in different file paths.

    Downstream ops can either load this DataFrame into a Pandas DataFrame or simply retrieve a path
    to where the data is stored.
    """

    def __init__(self, base_path: str, load_as_dataframe: bool = True):
        self._base_path = base_path
        self._load_as_dataframe = load_as_dataframe

    def handle_output(self, context: OutputContext, obj: pd.DataFrame):
        path = self._get_path(context)
        parent_path = path.parent
        if "://" not in self._base_path:
            parent_path.mkdir(mode=0o755, parents=True, exist_ok=True)

        if isinstance(obj, pd.DataFrame):
            row_count = len(obj)
            context.log.info(f"Row count: {row_count}")
            obj.to_parquet(path=path.as_posix(), index=False, compression="snappy")
        else:
            raise Exception(f"Outputs of type {type(obj)} not supported.")

        context.add_output_metadata({"row_count": row_count, "path": path.as_posix()})

    def load_input(self, context: InputContext) -> Union[pd.DataFrame, str]:
        path = self._get_path(context)
        if self._load_as_dataframe:
            return pd.read_parquet(path=path.as_posix())
        else:
            metadata_entries = get_output_metadata_entries(
                entry_keys=["path"], ctx=context.upstream_output
            )
            return metadata_entries["path"]

    def _get_path(self, context: Union[InputContext, OutputContext]) -> Path:
        key = context.asset_key.path[-1]

        if context.has_asset_partitions:
            start, end = context.asset_partitions_time_window
            dt_format = "%Y%m%d%H%M%S"
            partition_str = start.strftime(dt_format) + "_" + end.strftime(dt_format)
            return Path(self._base_path).joinpath(Path(key), Path(f"{partition_str}.parquet"))
        else:
            return Path(self._base_path).joinpath(Path(f"{key}.parquet"))


@io_manager(
    config_schema={
        "base_path": Field(
            str, description="The base path for store parquet files.", is_required=False
        ),
        "load_as_dataframe": Field(
            bool,
            description="""Indicates whether to load data as a Pandas DataFrame, defaults to True."
            Path to the parquet file will be returned if the value is False.
            """,
            default_value=True,
            is_required=False,
        ),
    },
)
def local_partitioned_parquet_io_manager(init_context):
    return PartitionedParquetIOManager(
        base_path=init_context.resource_config.get("base_path", get_system_temp_directory()),
        load_as_dataframe=init_context.resource_config.get("load_as_dataframe"),
    )
