from typing import Annotated

import pandas as pd
import pandera as pa
from pandera.typing import Series


class BronzeRainConditionSchema(pa.SchemaModel):
    """The schema created by Pandera for rain condition in the bronze layer."""

    lat: Series[pa.Float32] = pa.Field(ge=-90.0, le=90.0, description="Latitude", nullable=False)
    lon: Series[pa.Float32] = pa.Field(ge=-180.0, le=180.0, description="Longitude", nullable=False)
    locationName: Series[pa.String] = pa.Field(
        description="The name of the location.", nullable=False
    )
    stationId: Series[pa.String] = pa.Field(
        description="The station ID of the location.", nullable=False
    )
    CITY: Series[pa.String] = pa.Field(description="The name of the city.", nullable=False)
    CITY_SN: Series[pa.String] = pa.Field(
        description="The serial number of the city.", nullable=False
    )
    TOWN: Series[pa.String] = pa.Field(description="The name of the town.", nullable=False)
    TOWN_SN: Series[pa.String] = pa.Field(
        description="The serial number of the town.", nullable=False
    )
    obsTime: Series[Annotated[pd.DatetimeTZDtype, "ns", "Asia/Taipei"]] = pa.Field(
        description="The name of the location.", nullable=False
    )
    ELEV: Series[pa.Float32] = pa.Field(description="elev", nullable=False)
    RAIN: Series[pa.Float32] = pa.Field(description="rain", nullable=False)
    MIN_10: Series[pa.Float32] = pa.Field(description="min_10", nullable=False)
    HOUR_3: Series[pa.Float32] = pa.Field(description="hour_3", nullable=False)
    HOUR_6: Series[pa.Float32] = pa.Field(description="hour_6", nullable=False)
    HOUR_12: Series[pa.Float32] = pa.Field(description="hour_12", nullable=False)
    HOUR_24: Series[pa.Float32] = pa.Field(description="hour_24", nullable=False)
    NOW: Series[pa.Float32] = pa.Field(description="now", nullable=False)
    latest_2days: Series[pa.Float32] = pa.Field(description="latest 2 days", nullable=False)
    latest_3days: Series[pa.Float32] = pa.Field(description="latest 3 days", nullable=False)


class SilverWeatherSchema(pa.SchemaModel):
    county: Series[pd.StringDtype] = pa.Field(description="The county in Taiwan")
    site: Series[pd.StringDtype] = pa.Field(description="The site name.")
    temperature: Series[pa.Float32] = pa.Field(
        in_range={"min_value": -50, "max_value": 50},
        description="The value of temperature.",
        nullable=True,
    )
    humidity: Series[pa.Float32] = pa.Field(
        in_range={"min_value": 0, "max_value": 100},
        description="The value of humidity",
        nullable=True,
    )
    event_time: Series[pd.DatetimeTZDtype] = pa.Field(
        description="The event time.", dtype_kwargs={"tz": "Asia/Taipei"}
    )


class SilverRainSchema(pa.SchemaModel):
    county: Series[str] = pa.Field(description="The county in Taiwan")
    site: Series[str] = pa.Field(description="The site name.")
    rain: Series[pa.Float32] = pa.Field(description="The value of temperature.")
    event_time: Series[Annotated[pd.DatetimeTZDtype, "ns", "Asia/Taipei"]] = pa.Field(
        description="The event time."
    )


class GoldWeatherSchema(pa.SchemaModel):
    county: Series[str] = pa.Field(description="The county in Taiwan")
    site: Series[str] = pa.Field(description="The site name.")
    temperature: Series[pa.Float32] = pa.Field(
        in_range={"min_value": -50, "max_value": 50},
        description="The value of temperature.",
        nullable=True,
    )
    humidity: Series[pa.Float32] = pa.Field(
        in_range={"min_value": 0, "max_value": 100},
        description="The value of humidity",
        nullable=True,
    )
    rain: Series[pa.Float32] = pa.Field(description="The value of temperature.")
    event_time: Series[pd.Timestamp] = pa.Field(description="The event time.")
    # event_time: Series[pd.DatetimeTZDtype] = pa.Field(
    #     description="The event time.", dtype_kwargs={"tz": "Asia/Taipei"}
    # )
