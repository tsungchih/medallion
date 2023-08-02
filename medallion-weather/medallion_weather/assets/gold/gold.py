from datetime import datetime

import pandas as pd
import pendulum
from dagster import AssetIn, AssetKey, MetadataValue, OpExecutionContext, Output, asset

from medallion_weather.assets import GOLD_GROUP_NAME
from medallion_weather.typing import GoldWeatherSchemaType

from ..partitions import hourly_partitions_def

_gold_asset_metadata = {
    "org": "Home",
    "team": "Data Innovation",
    "contact": MetadataValue.url(url="mailto:tsungchih.hd@gmail.com"),
    "layer": GOLD_GROUP_NAME,
}


@asset(
    compute_kind="pandas",
    dagster_type=GoldWeatherSchemaType,
    key_prefix=["GCP", "test_pub_dataset"],
    metadata=_gold_asset_metadata | {"partition_expr": "EVENT_TIME"},
    io_manager_key="bq_io_manager",
    ins={
        "gold_aqi_with_pm_asset": AssetIn(
            key=AssetKey(["GCP", "test_pub_dataset", "gold_aqi_with_pm_asset"]),
            input_manager_key="bq_io_manager",
        )
    },
    partitions_def=hourly_partitions_def,
)
def gold_weather_asset(
    context: OpExecutionContext,
    silver_weather_asset,
    silver_rain_condition_asset,
    gold_aqi_with_pm_asset,
) -> Output[pd.DataFrame]:
    """This asset joined weather and rain condition information originated from the silver layer."""
    weather_df = gold_aqi_with_pm_asset.drop(labels=["event_time"], axis=1)
    silver_weather_df = silver_weather_asset.drop(labels=["event_time"], axis=1)

    df: pd.DataFrame = silver_weather_df.merge(
        silver_rain_condition_asset, on=["county", "site"], how="inner"
    ).merge(weather_df, on=["county", "site"], how="left")
    df["event_time"] = df["event_time"].apply(
        lambda x: datetime.fromisoformat(
            pendulum.from_format(string=context.partition_key, fmt="YYYY-MM-DD-HH:mm", tz="UTC")
            .add(minutes=30)
            .to_datetime_string()
        )
    )
    row_count, col_count = df.shape
    metadata = {
        "row_count": row_count,
        "col_count": col_count,
    }
    return Output(value=df, metadata=metadata)
