import numpy as np
import pandas as pd
from pandera import Field, SchemaModel
from pandera.typing import Series


class GoldAqiWithPmSchema(SchemaModel):
    """The schema class for AQI with PM table in the `Gold` layer."""

    site: Series[str] = Field(description="The name of site.")
    county: Series[str] = Field(description="The county of site.")
    pm25: Series[np.float32] = Field(
        ge=0, description="The value of PM2.5 with unit (μg/m3) measured by the site."
    )
    pm10: Series[np.float32] = Field(
        ge=0, description="The value of PM10 with unit (μg/m3) measured by the site."
    )
    aqi: Series[np.float32] = Field(ge=0, description="The value of AQI measured by the site.")
    event_time: Series[pd.Timestamp] = Field(description="The event time.")


class GoldAirWithAvgSchema(SchemaModel):
    """The schema class for AQI with PM table in the `Gold` layer."""

    site: Series[str] = Field(description="The name of site monitoring air status in average.")
    county: Series[str] = Field(description="The county where the site is located.")
    o3: Series[np.float32] = Field(ge=0, description="Average O3 for the latest 8 hours (ppb).")
    co: Series[np.float32] = Field(ge=0, description="Average CO for the latest 8 hours (ppm).")
    so2: Series[np.float32] = Field(ge=0, description="Average SO2 (ppb).")
    no: Series[np.float32] = Field(ge=0, description="NO (ppb).")
    no2: Series[np.float32] = Field(ge=0, description="NO2 (ppb).")
    nox: Series[np.float32] = Field(ge=0, description="NOX (ppb).")
    pollutant: Series[str] = Field(description="Pollutant indicator.")
    o3_8hr: Series[np.float32] = Field(ge=0, description="Average O3 for the latest 8 hours (ppb).")
    co_8hr: Series[np.float32] = Field(ge=0, description="Average CO for the latest 8 hours (ppm).")
    pm25_avg: Series[np.float32] = Field(ge=0, description="Average PM2.5 (μg/m3)")
    pm10_avg: Series[np.float32] = Field(ge=0, description="Average PM10 (μg/m3).")
    so2_avg: Series[np.float32] = Field(ge=0, description="Average SO2 (ppb).")
    event_time: Series[pd.Timestamp] = Field(description="The time when the event was published.")
