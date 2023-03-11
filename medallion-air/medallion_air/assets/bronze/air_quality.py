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

from .config import ApiConfig

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
    io_manager_key="parquet_io_manager",
    partitions_def=hourly_partitions_def,
)
def bronze_pm25_asset(_context: OpExecutionContext, config: ApiConfig) -> Output[pd.DataFrame]:
    """This asset conforms to the raw data retrieved PM2.5 information."""

    partition_key: str = _context.asset_partition_key_for_output()
    raw_contents = requests.get(url=config.api_uri).text
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
    io_manager_key="parquet_io_manager",
    partitions_def=hourly_partitions_def,
)
def bronze_pm10_asset(_context: OpExecutionContext, config: ApiConfig) -> Output[pd.DataFrame]:
    """This asset conforms to the raw data retrieved PM10 information."""

    raw_contents = requests.get(url=config.api_uri).text
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
    io_manager_key="parquet_io_manager",
    partitions_def=hourly_partitions_def,
)
def bronze_aqi_asset(_context: OpExecutionContext, config: ApiConfig) -> Output[pd.DataFrame]:
    """This asset conforms to the raw data retrieved AQI information."""

    raw_contents = requests.get(url=config.api_uri).text
    table: AirQualityTableBase = table_factory.create_object(AirQualityTableType.AQI, raw_contents)
    table.discover()

    return Output(value=table.df, metadata=table.metadata)
