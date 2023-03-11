import os

import pandas as pd
import requests
from dagster import Field, MetadataValue, OpExecutionContext, Output, asset

from medallion_air.assets.partitions import hourly_partitions_def
from medallion_air.schemas.air_quality_tables import AirQualityTableBase
from medallion_air.schemas.factory import AirQualityTableFactory
from medallion_air.typing import (
    AirQualityTableType,
    BronzeAqiTableSchemaType,
    BronzePm10TableSchemaType,
    BronzePm25TableSchemaType,
)

table_factory: AirQualityTableFactory = AirQualityTableFactory()


@asset(
    compute_kind="python",
    dagster_type=BronzePm25TableSchemaType,
    metadata={
        "org": "Home",
        "team": "Data Innovation",
        "loc": "Taiwan",
        "contact": MetadataValue.url(url="mailto:tsungchih.hd@gmail.com"),
        "layer": "bronze",
        "frequency": "per hour",
    },
    config_schema={
        "api_uri": Field(
            str,
            default_value=os.environ.get("MEDALLION_AIR_PM25_URI"),
            description="the URL for getting the raw data.",
        ),
    },
    io_manager_key="parquet_io_manager",
    partitions_def=hourly_partitions_def,
)
def bronze_pm25_asset(_context: OpExecutionContext) -> Output[pd.DataFrame]:
    """This asset conforms to the raw data retrieved PM2.5 information."""

    partition_key: str = _context.asset_partition_key_for_output()
    raw_contents = requests.get(url=_context.op_config["api_uri"]).text
    table: AirQualityTableBase = table_factory.create_object(AirQualityTableType.PM25, raw_contents)
    table.discover()

    return Output(value=table.df, metadata=table.metadata)


@asset(
    compute_kind="python",
    dagster_type=BronzePm10TableSchemaType,
    metadata={
        "org": "Home",
        "team": "Data Innovation",
        "loc": "Taiwan",
        "contact": MetadataValue.url(url="mailto:tsungchih.hd@gmail.com"),
        "layer": "bronze",
        "frequency": "per hour",
    },
    config_schema={
        "api_uri": Field(
            str,
            default_value=os.environ.get("MEDALLION_AIR_PM10_URI"),
            description="the URL for getting the raw data.",
        ),
    },
    io_manager_key="parquet_io_manager",
    partitions_def=hourly_partitions_def,
)
def bronze_pm10_asset(_context: OpExecutionContext) -> Output[pd.DataFrame]:
    """This asset conforms to the raw data retrieved PM10 information."""

    raw_contents = requests.get(url=_context.op_config["api_uri"]).text
    table: AirQualityTableBase = table_factory.create_object(AirQualityTableType.PM10, raw_contents)
    table.discover()

    return Output(value=table.df, metadata=table.metadata)


@asset(
    compute_kind="python",
    dagster_type=BronzeAqiTableSchemaType,
    metadata={
        "org": "Home",
        "team": "Data Innovation",
        "loc": "Taiwan",
        "contact": MetadataValue.url(url="mailto:tsungchih.hd@gmail.com"),
        "layer": "bronze",
        "frequency": "per hour",
    },
    config_schema={
        "api_uri": Field(
            str,
            default_value=os.environ.get("MEDALLION_AIR_AQI_URI"),
            description="the URL for getting the raw data.",
        ),
    },
    io_manager_key="parquet_io_manager",
    partitions_def=hourly_partitions_def,
)
def bronze_aqi_asset(_context: OpExecutionContext) -> Output[pd.DataFrame]:
    """This asset conforms to the raw data retrieved AQI information."""

    raw_contents = requests.get(url=_context.op_config["api_uri"]).text
    table: AirQualityTableBase = table_factory.create_object(AirQualityTableType.AQI, raw_contents)
    table.discover()

    return Output(value=table.df, metadata=table.metadata)
