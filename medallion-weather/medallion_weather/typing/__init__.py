from enum import Enum

from dagster_pandas import PandasColumn, create_dagster_pandas_dataframe_type
from dagster_pandera import pandera_schema_to_dagster_type
from pandas import DataFrame

from .schemas import (
    BronzeRainConditionSchema,
    GoldWeatherSchema,
    SilverRainSchema,
    SilverWeatherSchema,
)


class WeatherTableType(Enum):
    WEATHER = 1
    RAIN = 2


def bronze_weather_summary_stats(df: DataFrame):
    row_count, col_count = df.shape
    metadata = {
        "unique_city_count": str(df["CITY"].nunique()),
        "row_count": row_count,
        "col_count": col_count,
    }

    return metadata


BronzeWeatherSchemaType = create_dagster_pandas_dataframe_type(
    name="BronzeWeatherSchemaType",
    description="The weather schema type created by dagster-pandas.",
    columns=[
        PandasColumn.float_column(
            name="lat", non_nullable=True, is_required=True, min_value=-90.0, max_value=90.0
        ),
        PandasColumn.float_column(
            name="lon", non_nullable=True, is_required=True, min_value=-180.0, max_value=180.0
        ),
        PandasColumn.string_column(name="locationName", non_nullable=True, is_required=True),
        PandasColumn.string_column(name="stationId", non_nullable=True, is_required=True),
        PandasColumn.string_column(name="CITY", non_nullable=True, is_required=True),
        PandasColumn.string_column(name="CITY_SN", non_nullable=True, is_required=True),
        PandasColumn.string_column(name="TOWN", non_nullable=True, is_required=True),
        PandasColumn.string_column(name="TOWN_SN", non_nullable=True, is_required=True),
        PandasColumn.datetime_column(
            name="obsTime", non_nullable=True, is_required=True, tz="Asia/Taipei"
        ),
        PandasColumn.float_column(name="ELEV", non_nullable=True, is_required=True),
        PandasColumn.float_column(
            name="WDIR",
            is_required=True,
            min_value=0,
            max_value=360,
            ignore_missing_vals=True,
        ),
        PandasColumn.float_column(name="WDSD", is_required=True, ignore_missing_vals=True),
        PandasColumn.float_column(
            name="TEMP",
            is_required=True,
            min_value=-50.0,
            max_value=50.0,
            ignore_missing_vals=True,
        ),
        PandasColumn.float_column(
            name="HUMD",
            is_required=True,
            min_value=0.0,
            max_value=100.0,
            ignore_missing_vals=True,
        ),
        PandasColumn.float_column(name="PRES", non_nullable=True, is_required=True),
        PandasColumn.float_column(name="H_24R", non_nullable=True, is_required=True),
        PandasColumn.float_column(name="H_FX", non_nullable=True, is_required=True),
        PandasColumn.float_column(name="H_XD", non_nullable=True, is_required=True),
        PandasColumn.string_column(name="H_FXT", non_nullable=True, is_required=True),
        PandasColumn.float_column(name="D_TX", non_nullable=True, is_required=True),
        PandasColumn.datetime_column(
            name="D_TXT", non_nullable=True, is_required=True, tz="Asia/Taipei"
        ),
        PandasColumn.float_column(name="D_TN", non_nullable=True, is_required=True),
        PandasColumn.datetime_column(
            name="D_TNT", non_nullable=True, is_required=True, tz="Asia/Taipei"
        ),
    ],
    metadata_fn=bronze_weather_summary_stats,
)

BronzeRainConditionSchemaType = pandera_schema_to_dagster_type(BronzeRainConditionSchema)
SilverWeatherSchemaType = pandera_schema_to_dagster_type(SilverWeatherSchema)
SilverRainSchemaType = pandera_schema_to_dagster_type(SilverRainSchema)
GoldWeatherSchemaType = pandera_schema_to_dagster_type(GoldWeatherSchema)
