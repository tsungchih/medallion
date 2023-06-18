from datetime import datetime
from typing import Optional

from dagster_gcp_pandas import BigQueryPandasIOManager
from pydantic import Field

from dagster import Config, EnvVar, RunConfig, hourly_partitioned_config
from medallion_air.assets.bronze.config import ApiConfig
from medallion_air.assets.partitions import hourly_partitions_def


class PurgeAfterDaysResourceConfig(Config):
    success: Optional[int] = Field(
        default=-1,
        description=(
            "How many days job runs with a given status can be removed. A value of"
            "-1 indicates that job runs with a given status should be retained indefinitely."
        ),
        ge=-1,
    )
    failure: Optional[int] = Field(
        default=-1,
        description=(
            "How many days job runs with a given status can be removed. A value of"
            "-1 indicates that job runs with a given status should be retained indefinitely."
        ),
        ge=-1,
    )
    canceled: Optional[int] = Field(
        default=-1,
        description=(
            "How many days job runs with a given status can be removed. A value of"
            "-1 indicates that job runs with a given status should be retained indefinitely."
        ),
        ge=-1,
    )


class RetentionResourceConfig(Config):
    purge_after_days: PurgeAfterDaysResourceConfig


class JobCleanOpConfig(Config):
    job_name: str = Field(default=..., description="The job name to be filtered and cleaned.")
    retention: RetentionResourceConfig


@hourly_partitioned_config(
    start_date=hourly_partitions_def.get_first_partition_window(datetime.now()).start,
    timezone="Asia/Taipei",
)
def partitioned_all_air_assets_job_config(start: datetime, _end: datetime):
    resources_config = {
        "bq_io_manager": BigQueryPandasIOManager(
            project=EnvVar("GOOGLE_CLOUD_PROJECT"),
            location="us-west1",
            timeout=10.0,
        )
    }
    ops_config = {
        "bronze_aqi_asset": ApiConfig(api_uri=EnvVar("MEDALLION_AIR_AQI_URI")),
        "bronze_pm10_asset": ApiConfig(api_uri=EnvVar("MEDALLION_AIR_PM10_URI")),
        "bronze_pm25_asset": ApiConfig(api_uri=EnvVar("MEDALLION_AIR_PM25_URI")),
    }

    return RunConfig(ops=ops_config, resources=resources_config).to_config_dict()
