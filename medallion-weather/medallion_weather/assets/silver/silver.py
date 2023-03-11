import pandas as pd
from dagster import MetadataValue, OpExecutionContext, Output, asset

from medallion_weather.assets import SILVER_GROUP_NAME
from medallion_weather.assets.external import medallion_air_assets
from medallion_weather.typing import SilverRainSchemaType, SilverWeatherSchemaType

_silver_asset_metadata = {
    "org": "Home",
    "team": "Data Innovation",
    "contact": MetadataValue.url(url="mailto:tsungchih.hd@gmail.com"),
    "layer": SILVER_GROUP_NAME,
}


@asset(
    compute_kind="python",
    dagster_type=SilverWeatherSchemaType,
    metadata=_silver_asset_metadata,
    partitions_def=medallion_air_assets.hourly_partitions_def,
)
def silver_weather_asset(bronze_weather_asset) -> Output[pd.DataFrame]:
    """This asset filters out relevant columns from weather asset in the bronze layer.

    The following columns are extracted and renamed for consistency:
    - `CITY` --> `county`
    - `locationName` --> `site`
    - `obsTime` --> `event_time`
    - `TEMP` --> `temperature`
    - `HUMD` --> `humidity`
    """
    relevant_cols = ["CITY", "locationName", "obsTime", "TEMP", "HUMD"]
    column_mappings = {
        "CITY": "county",
        "locationName": "site",
        "obsTime": "event_time",
        "TEMP": "temperature",
        "HUMD": "humidity",
    }
    df: pd.DataFrame = bronze_weather_asset[relevant_cols]
    df = df.rename(columns=column_mappings)
    row_count, col_count = df.shape
    metadata = {
        "row_count": row_count,
        "col_count": col_count,
    }
    return Output(value=df, metadata=metadata)


@asset(
    compute_kind="python",
    dagster_type=SilverRainSchemaType,
    metadata=_silver_asset_metadata,
    partitions_def=medallion_air_assets.hourly_partitions_def,
)
def silver_rain_condition_asset(bronze_rain_condition_asset) -> Output[pd.DataFrame]:
    """This asset filters out relevant columns from rain condition asset in the bronze layer.

    The following columns are extracted and renamed for consistency:
    - `CITY` --> `county`
    - `locationName` --> `site`
    - `obsTime` --> `event_time`
    - `RAIN` --> `rain`
    """
    relevant_cols = ["CITY", "locationName", "obsTime", "RAIN"]
    column_mappings = {
        "CITY": "county",
        "locationName": "site",
        "obsTime": "event_time",
        "RAIN": "rain",
    }
    df: pd.DataFrame = bronze_rain_condition_asset[relevant_cols]
    df = df.rename(columns=column_mappings)
    row_count, col_count = df.shape
    metadata = {
        "row_count": row_count,
        "col_count": col_count,
    }
    return Output(value=df, metadata=metadata)
