import numpy as np
import pandas as pd
from pandera import Field, SchemaModel
from pandera.typing import Series


class BronzePm25TableSchema(SchemaModel):
    """Class for Pm25Table schema."""

    site: Series[str] = Field(description="The name of site monitoring PM2.5.")
    county: Series[str] = Field(description="The county where the site is located.")
    pm25: Series[np.float32] = Field(
        ge=0, description="The value with unit (μg/m3) which is measured by the site."
    )
    datacreationdate: Series[pd.Timestamp] = Field(
        description="The time when the event was published."
    )
    itemunit: Series[str] = Field(description="The unit of the item.")


class BronzePm10TableSchema(SchemaModel):
    """Class for Pm10Table schema."""

    siteid: Series[np.int8] = Field(description="The site ID.")
    sitename: Series[str] = Field(description="The name of the site.")
    county: Series[str] = Field(description="The county where the site is located.")
    itemid: Series[np.int8] = Field(description="The item ID.")
    itemname: Series[str] = Field(description="The name of the item.")
    itemengname: Series[str] = Field(description="The English name of the item.")
    itemunit: Series[str] = Field(description="The unit of the item.")
    monitordate: Series[pd.Timestamp] = Field(description="The date when the item was monitored.")
    concentration: Series[np.float32] = Field(ge=-1, description="The value of PM10.")


class BronzeAqiTableSchema(SchemaModel):
    """Class for AqiTable Schema."""

    sitename: Series[str] = Field(description="The name of the site. 測站名稱")
    county: Series[str] = Field(description="The county where the site is located.")
    aqi: Series[np.float32] = Field(ge=0, description="The value of AQI. 空氣品質指標")
    pollutant: Series[str] = Field(description="The value of pollutant. 空氣污染指標物")
    status: Series[str] = Field(description="The status in terms of the value of AQI. 狀態")
    so2: Series[np.float32] = Field(ge=0, description="The value of SO2 (ppb). 二氧化硫")
    co: Series[np.float32] = Field(ge=0, description="The value of CO (ppm). 一氧化碳")
    o3: Series[np.float32] = Field(ge=0, description="The value of O3 (ppb). 臭氧")
    o3_8hr: Series[np.float32] = Field(
        ge=0, description="The average value of O3 (ppb) for the latest 8 hours. 臭氧8小時移動平均"
    )
    pm10: Series[np.float32] = Field(ge=0, description="The value of PM10 (μg/m3). 懸浮微粒")
    pm25: Series[np.float32] = Field(ge=0, description="The value of PM2.5 (μg/m3). 細懸浮微粒")
    no2: Series[np.float32] = Field(ge=0, description="The value of NO2 (ppb). 二氧化氮")
    nox: Series[np.float32] = Field(ge=0, description="The value of NOX (ppb). 氮氧化物")
    no: Series[np.float32] = Field(ge=0, description="The value of NO (ppb). 一氧化氮")
    wind_speed: Series[np.float32] = Field(
        ge=0, nullable=True, description="The value of wind speed (m/sec). 風速"
    )
    wind_direc: Series[np.int8] = Field(
        in_range={"min_value": -360, "max_value": 360},
        nullable=True,
        description="The value of wind direction (degrees). 風向",
    )
    publishtime: Series[pd.Timestamp] = Field(
        description="The date time when the record was published."
    )
    co_8hr: Series[np.float32] = Field(
        ge=0, description="The value of CO (ppm) for the latest 8 hours. 一氧化碳8小時移動平均"
    )
    pm25_avg: Series[np.float32] = Field(
        ge=0, description="The average value of PM2.5 (μg/m3) for the latest 8 hours. 細懸浮微粒移動平均值"
    )
    pm10_avg: Series[np.float32] = Field(
        ge=0, description="The average value of PM10 (μg/m3) for the latest 8 hours. 懸浮微粒移動平均值"
    )
    so2_avg: Series[np.float32] = Field(
        ge=0, nullable=True, description="The average value of SO2 (ppb). 二氧化硫移動平均值"
    )
    longitude: Series[np.float32] = Field(ge=0, description="The longitude of the site. 經度")
    latitude: Series[np.float32] = Field(ge=0, description="The latitude of the site. 緯度")
    siteid: Series[np.int8] = Field(description="The site ID.")
