import requests
from dagster import MetadataValue, OpExecutionContext, Output, asset
from pandas import DataFrame

from medallion_weather.assets import BRONZE_GROUP_NAME
from medallion_weather.assets.external import medallion_air_assets
from medallion_weather.resources.configs import ApiOpsConfig
from medallion_weather.schemas.factory import WeatherTableFactory
from medallion_weather.schemas.weather_tables import BronzeWeatherTableBase
from medallion_weather.typing import (
    BronzeRainConditionSchemaType,
    BronzeWeatherSchemaType,
    WeatherTableType,
)

table_factory: WeatherTableFactory = WeatherTableFactory()

_bronze_asset_metadata = {
    "org": "Home",
    "team": "Data Innovation",
    "contact": MetadataValue.url(url="mailto:tsungchih.hd@gmail.com"),
    "layer": BRONZE_GROUP_NAME,
}


@asset(
    compute_kind="python",
    dagster_type=BronzeWeatherSchemaType,
    metadata=_bronze_asset_metadata,
    partitions_def=medallion_air_assets.hourly_partitions_def,
)
def bronze_weather_asset(context: OpExecutionContext, config: ApiOpsConfig) -> Output[DataFrame]:
    """This asset holds the weather information retrieved from the given weather API."""

    partition_key_str = context.asset_partition_key_for_output()
    context.log.info(f"The partition key for bronze_weather_asset: {partition_key_str}.")
    api_uri = config.api_uri
    try:
        raw_contents = requests.get(api_uri).text
    except requests.URLRequired as e:
        raise e
    else:
        table: BronzeWeatherTableBase = table_factory.create_object(
            otype=WeatherTableType.WEATHER, contents=raw_contents
        )
        table.discover()
        return Output(value=table.df, metadata=table.metadata)


@asset(
    compute_kind="python",
    dagster_type=BronzeRainConditionSchemaType,
    metadata=_bronze_asset_metadata,
    partitions_def=medallion_air_assets.hourly_partitions_def,
)
def bronze_rain_condition_asset(
    context: OpExecutionContext, config: ApiOpsConfig
) -> Output[DataFrame]:
    """This asset holds the rain condition information retrieved from the given API."""

    api_uri = config.api_uri
    try:
        raw_contents = requests.get(api_uri).text
    except requests.URLRequired as e:
        raise e
    else:
        table: BronzeWeatherTableBase = table_factory.create_object(
            otype=WeatherTableType.RAIN, contents=raw_contents
        )
        table.discover()
        return Output(value=table.df, metadata=table.metadata)
