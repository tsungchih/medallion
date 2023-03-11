import os

import pandas as pd
from dagster import Output, build_op_context
from dotenv import load_dotenv

from medallion_air.assets.bronze.air_quality import (
    bronze_aqi_asset,
    bronze_pm10_asset,
    bronze_pm25_asset,
)

load_dotenv()


def test_bronze_pm25_asset():
    op_config = {"api_uri": os.environ.get("MEDALLION_AIR_PM25_URI")}
    ctx = build_op_context(op_config=op_config)
    out: Output[pd.DataFrame] = bronze_pm25_asset(ctx)
    assert out.value.shape[0] > 0


def test_bronze_pm10_asset():
    op_config = {"api_uri": os.environ.get("MEDALLION_AIR_PM10_URI")}
    ctx = build_op_context(op_config=op_config)
    out: Output[pd.DataFrame] = bronze_pm10_asset(ctx)
    assert out.value.shape[0] > 0


def test_bronze_aqi_asset():
    op_config = {"api_uri": os.environ.get("MEDALLION_AIR_AQI_URI")}
    ctx = build_op_context(op_config=op_config)
    out: Output[pd.DataFrame] = bronze_aqi_asset(ctx)
    assert out.value.shape[0] > 0
