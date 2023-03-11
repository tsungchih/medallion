import numpy as np
import pandas as pd
from dagster import (
    AssetOut,
    MetadataValue,
    OpExecutionContext,
    Output,
    asset,
    multi_asset,
)

from medallion_air.assets.partitions import hourly_partitions_def
from medallion_air.typing import (
    SilverAirAvgTableSchemaType,
    SilverAirTableSchemaType,
    SilverAqiTableSchemaType,
    SilverPm10TableSchemaType,
    SilverPm25TableSchemaType,
    SilverWindTableSchemaType,
)


@asset(
    compute_kind="python",
    dagster_type=SilverPm25TableSchemaType,
    metadata={
        "org": "Home",
        "team": "Data Innovation",
        "loc": "Taiwan",
        "contact": MetadataValue.url(url="mailto:tsungchih.hd@gmail.com"),
        "layer": "silver",
        "frequency": "per hour",
    },
    partitions_def=hourly_partitions_def,
)
def silver_pm25_asset(_context: OpExecutionContext, bronze_pm25_asset) -> Output[pd.DataFrame]:
    """This asset conforms to the raw data retrieved PM2.5 information."""
    df = bronze_pm25_asset.rename(columns={"datacreationdate": "event_time"})
    df.drop(labels=["itemunit"], axis=1, inplace=True)
    df["pm25"] = df["pm25"].replace(to_replace="", value=np.nan)
    df["pm25"] = pd.to_numeric(df["pm25"], downcast="float")
    df["event_time"] = df["event_time"].apply(pd.to_datetime)
    df.dropna(inplace=True)
    return Output(value=df, metadata={"row_count": df.shape[0]})


@asset(
    compute_kind="python",
    dagster_type=SilverPm10TableSchemaType,
    metadata={
        "org": "Home",
        "team": "Data Innovation",
        "loc": "Taiwan",
        "contact": MetadataValue.url(url="mailto:tsungchih.hd@gmail.com"),
        "layer": "silver",
        "frequency": "per hour",
    },
    partitions_def=hourly_partitions_def,
)
def silver_pm10_asset(_context: OpExecutionContext, bronze_pm10_asset) -> Output[pd.DataFrame]:
    """This asset conforms to the raw data retrieved PM10 information."""
    df = bronze_pm10_asset.drop(
        labels=["siteid", "itemid", "itemname", "itemengname", "itemunit"], axis=1
    )
    df.rename(
        columns={"sitename": "site", "concentration": "pm10", "monitordate": "event_time"},
        inplace=True,
    )
    df["pm10"].replace(to_replace="x", value=np.nan, inplace=True)
    df["pm10"] = pd.to_numeric(df["pm10"], downcast="float")
    df["event_time"] = df["event_time"].apply(pd.to_datetime)
    df.dropna(inplace=True)
    return Output(value=df, metadata={"row_count": df.shape[0]})


@multi_asset(
    compute_kind="python",
    outs={
        "silver_wind_asset": AssetOut(
            dagster_type=SilverWindTableSchemaType,
            description="This asset describes the wind condition.",
        ),
        "silver_aqi_asset": AssetOut(
            dagster_type=SilverAqiTableSchemaType,
            description="This asset describes the AQI condition for each site.",
        ),
        "silver_air_asset": AssetOut(
            dagster_type=SilverAirTableSchemaType,
            description="This asset describes the air condition for each site.",
        ),
        "silver_air_avg_asset": AssetOut(
            dagster_type=SilverAirAvgTableSchemaType,
            description="This asset describes the air condition in average for each site.",
        ),
    },
    partitions_def=hourly_partitions_def,
)
def silver_aqi_multi_asset(_context: OpExecutionContext, bronze_aqi_asset):
    """This asset produces multiple assets from bronze_aqi_asset."""
    aqi_table_cols = ["sitename", "county", "aqi", "publishtime"]
    wind_table_cols = ["sitename", "county", "wind_speed", "wind_direc", "publishtime"]
    air_table_cols = [
        "sitename",
        "county",
        "o3",
        "co",
        "so2",
        "no",
        "no2",
        "nox",
        "pollutant",
        "publishtime",
    ]
    air_avg_table_cols = [
        "sitename",
        "county",
        "o3_8hr",
        "co_8hr",
        "pm25_avg",
        "pm10_avg",
        "so2_avg",
        "publishtime",
    ]

    df: pd.DataFrame = bronze_aqi_asset[wind_table_cols]
    wind_df = df.rename(
        columns={"sitename": "site", "wind_direc": "wind_dir", "publishtime": "event_time"}
    )
    wind_df.dropna(inplace=True)

    df = bronze_aqi_asset[aqi_table_cols]
    aqi_df = df.rename(columns={"sitename": "site", "publishtime": "event_time"})
    aqi_df["aqi"] = aqi_df["aqi"].replace(to_replace="", value=np.nan)

    df = bronze_aqi_asset[air_table_cols]
    air_df = df.rename(columns={"sitename": "site", "publishtime": "event_time"})
    air_df.dropna(inplace=True)

    df = bronze_aqi_asset[air_avg_table_cols]
    air_avg_df = df.rename(columns={"sitename": "site", "publishtime": "event_time"})
    air_avg_df.dropna(inplace=True)

    yield Output(
        value=wind_df,
        output_name="silver_wind_asset",
        metadata={"row_count": wind_df.shape[0], "col_count": wind_df.shape[1]},
    )
    yield Output(
        value=aqi_df,
        output_name="silver_aqi_asset",
        metadata={"row_count": aqi_df.shape[0], "col_count": aqi_df.shape[1]},
    )
    yield Output(
        value=air_df,
        output_name="silver_air_asset",
        metadata={"row_count": air_df.shape[0], "col_count": aqi_df.shape[1]},
    )
    yield Output(
        value=air_avg_df,
        output_name="silver_air_avg_asset",
        metadata={"row_count": air_avg_df.shape[0], "col_count": air_avg_df.shape[1]},
    )
