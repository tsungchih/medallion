import numpy as np
import pandas as pd
from pandera import Field, SchemaModel
from pandera.typing import Series


class SilverPm25TableSchema(SchemaModel):
    """Class for Pm25Table schema."""

    site: Series[str] = Field(description="The name of site monitoring PM2.5.")
    county: Series[str] = Field(description="The county where the site is located.")
    pm25: Series[np.float32] = Field(
        ge=0, description="The value of PM2.5 with unit (μg/m3) measured by the site."
    )
    event_time: Series[pd.Timestamp] = Field(description="The time when the event was published.")


class SilverPm10TableSchema(SchemaModel):
    """Class for Pm10Table schema."""

    site: Series[str] = Field(description="The name of site monitoring PM10.")
    county: Series[str] = Field(description="The county where the site is located.")
    pm10: Series[np.float32] = Field(
        ge=0, description="The value of PM10 with unit (μg/m3) measured by the site."
    )
    event_time: Series[pd.Timestamp] = Field(description="The time when the event was published.")


class SilverAqiTableSchema(SchemaModel):
    """Class for AqiTable Schema."""

    site: Series[str] = Field(description="The name of site monitoring AQI.")
    county: Series[str] = Field(description="The county where the site is located.")
    aqi: Series[np.float32] = Field(ge=0, description="The value of AQI measured by the site.")
    event_time: Series[pd.Timestamp] = Field(description="The time when the event was published.")


class SilverWindTableSchema(SchemaModel):
    """Class for WindTable Schema."""

    site: Series[str] = Field(description="The name of site monitoring wind.")
    county: Series[str] = Field(description="The county where the site is located.")
    wind_speed: Series[np.float32] = Field(ge=0, description="The wind speed with unit (m/sec).")
    wind_dir: Series[np.int8] = Field(description="The wind direction with degrees unit.")
    event_time: Series[pd.Timestamp] = Field(description="The time when the event was published.")


class SilverAirTableSchema(SchemaModel):
    """Class for AirTable schema."""

    site: Series[str] = Field(description="The name of site monitoring air status in average.")
    county: Series[str] = Field(description="The county where the site is located.")
    o3: Series[np.float32] = Field(ge=0, description="Average O3 for the latest 8 hours (ppb).")
    co: Series[np.float32] = Field(ge=0, description="Average CO for the latest 8 hours (ppm).")
    so2: Series[np.float32] = Field(ge=0, description="Average SO2 (ppb).")
    no: Series[np.float32] = Field(ge=0, description="NO (ppb).")
    no2: Series[np.float32] = Field(ge=0, description="NO2 (ppb).")
    nox: Series[np.float32] = Field(ge=0, description="NOX (ppb).")
    pollutant: Series[str] = Field(description="Pollutant indicator.")
    event_time: Series[pd.Timestamp] = Field(description="The time when the event was published.")


class SilverAvgTableSchema(SchemaModel):
    """Class for AirAvgTable Schema."""

    site: Series[str] = Field(description="The name of site monitoring air status in average.")
    county: Series[str] = Field(description="The county where the site is located.")
    o3_8hr: Series[np.float32] = Field(ge=0, description="Average O3 for the latest 8 hours (ppb).")
    co_8hr: Series[np.float32] = Field(ge=0, description="Average CO for the latest 8 hours (ppm).")
    pm25_avg: Series[np.float32] = Field(ge=0, description="Average PM2.5 (μg/m3)")
    pm10_avg: Series[np.float32] = Field(ge=0, description="Average PM10 (μg/m3).")
    so2_avg: Series[np.float32] = Field(ge=0, description="Average SO2 (ppb).")
    event_time: Series[pd.Timestamp] = Field(description="The time when the event was published.")
