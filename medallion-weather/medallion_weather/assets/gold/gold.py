import pandas as pd
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
    compute_kind="python",
    dagster_type=GoldWeatherSchemaType,
    metadata=_gold_asset_metadata,
    ins={
        "gold_aqi_with_pm_asset": AssetIn(
            key=AssetKey(["GCP", "test_pub_dataset", "gold_aqi_with_pm_asset"])
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
    context.log.info(df.head())
    df["event_time"] = df["event_time"].replace(to_replace=[None], value=df.event_time.mode())

    row_count, col_count = df.shape
    metadata = {
        "row_count": row_count,
        "col_count": col_count,
    }
    return Output(value=df, metadata=metadata)
