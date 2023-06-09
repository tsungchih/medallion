from datetime import datetime

import pendulum
from pandas import DataFrame

from dagster import MetadataValue, OpExecutionContext, Output, asset
from medallion_air.assets.partitions import hourly_partitions_def
from medallion_air.typing import GoldAirWithAvgSchemaType, GoldAqiWithPmSchemaType


@asset(
    compute_kind="python",
    dagster_type=GoldAqiWithPmSchemaType,
    key_prefix=["test_pub_dataset"],
    io_manager_key="bq_io_manager",
    metadata={
        "org": "Home",
        "team": "Data Innovation",
        "loc": "Taiwan",
        "contact": MetadataValue.url(url="mailto:tsungchih.hd@gmail.com"),
        "layer": "gold",
        "frequency": "per hour",
        "partition_expr": "EVENT_TIME",
    },
    partitions_def=hourly_partitions_def,
)
def gold_aqi_with_pm_asset(
    _context: OpExecutionContext, silver_pm25_asset, silver_pm10_asset, silver_aqi_asset
) -> Output[DataFrame]:
    """This asset describes AQI, PM10, and PM2.5 conditions for each site."""
    idx = ("site", "county")

    df: DataFrame = (
        silver_pm25_asset.merge(silver_pm10_asset, on=idx)
        .merge(silver_aqi_asset, on=idx)
        .drop(labels=["event_time_x", "event_time_y"], axis=1)
    )
    df["event_time"] = df["event_time"].apply(
        lambda x: datetime.fromisoformat(
            pendulum.from_format(string=_context.partition_key, fmt="YYYY-MM-DD-HH:mm", tz="UTC")
            .add(minutes=30)
            .to_datetime_string()
        )
    )

    return Output(value=df, metadata={"row_count": df.shape[0], "col_count": df.shape[1]})


@asset(
    compute_kind="python",
    dagster_type=GoldAirWithAvgSchemaType,
    key_prefix=["test_pub_dataset"],
    io_manager_key="bq_io_manager",
    metadata={
        "org": "Home",
        "team": "Data Innovation",
        "loc": "Taiwan",
        "contact": MetadataValue.url(url="mailto:tsungchih.hd@gmail.com"),
        "layer": "gold",
        "frequency": "per hour",
        "partition_expr": "event_time",
    },
    partitions_def=hourly_partitions_def,
)
def gold_air_with_avg_asset(
    _context: OpExecutionContext, silver_air_asset, silver_air_avg_asset
) -> Output[DataFrame]:
    """This data product provides air conditions based on average values."""
    idx = ("site", "county")

    df: DataFrame = (
        silver_air_asset.merge(silver_air_avg_asset, on=idx)
        .rename(columns={"event_time_x": "event_time"})
        .drop(labels=["event_time_y"], axis=1)
    )
    df["event_time"] = df["event_time"].apply(
        lambda x: datetime.fromisoformat(
            pendulum.from_format(string=_context.partition_key, fmt="YYYY-MM-DD-HH:mm", tz="UTC")
            .add(minutes=30)
            .to_datetime_string()
        )
    )

    return Output(value=df, metadata={"row_count": df.shape[0], "col_count": df.shape[1]})
