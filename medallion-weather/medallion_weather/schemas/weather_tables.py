from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Dict, List, Optional

import numpy as np
import orjson
import pandas as pd


@dataclass
class AbstractDataclass(ABC):
    def __new__(cls, *args, **kwargs):
        if cls == AbstractDataclass or cls.__bases__[0] == AbstractDataclass:
            raise TypeError("Cannot instantiate abstract class.")
        return super().__new__(cls)


@dataclass
class BronzeWeatherTableBase(AbstractDataclass):
    _raw_contents: str
    _df: Optional[pd.DataFrame] = field(init=False)
    _metadata: Optional[Dict[str, str]] = field(init=False)
    _df_astype: Optional[Dict[str, str]] = field(init=False)

    @abstractmethod
    def discover(self) -> None:
        """Discover DataFrame and metadata from the `self._raw_contentx`."""
        raise NotImplementedError("You have to implement this method.")

    @property
    @abstractmethod
    def df(self) -> pd.DataFrame:
        """Return the discovered DataFrame object."""
        raise NotImplementedError("You have to implement this method to derive a Pandas DataFrame.")

    @property
    @abstractmethod
    def metadata(self) -> Dict:
        """Return the metadata of the discovered DataFrame object"""
        raise NotImplementedError("You have to implement this method to derive a Pandas DataFrame.")


@dataclass
class BronzeWeatherTable(BronzeWeatherTableBase):
    def __post_init__(self) -> None:
        self._df_astype = {
            "lat": "float32",
            "lon": "float32",
            "locationName": "string",
            "stationId": "string",
            "CITY": "string",
            "CITY_SN": "string",
            "TOWN": "string",
            "TOWN_SN": "string",
            "obsTime": "datetime64[ns, Asia/Taipei]",
            "ELEV": "float32",
            "WDIR": "float32",
            "WDSD": "float32",
            "TEMP": "float32",
            "HUMD": "float32",
            "PRES": "float32",
            "H_24R": "float32",
            "H_FX": "float32",
            "H_XD": "float32",
            "H_FXT": "string",
            "D_TX": "float32",
            "D_TXT": "datetime64[ns, Asia/Taipei]",
            "D_TN": "float32",
            "D_TNT": "datetime64[ns, Asia/Taipei]",
        }

    def discover(self) -> None:
        data: List[Dict[str, str]] = []
        try:
            json_obj = orjson.loads(self._raw_contents)
        except orjson.JSONEncodeError as e:
            raise e
        else:
            locations = json_obj.get("records").get("location")
            for location in locations:
                row = {
                    "lat": location["lat"],
                    "lon": location["lon"],
                    "locationName": location["locationName"],
                    "stationId": location["stationId"],
                    "obsTime": location["time"]["obsTime"],
                }
                for item in location["weatherElement"]:
                    row[item["elementName"]] = item["elementValue"]
                for item in location["parameter"]:
                    row[item["parameterName"]] = item["parameterValue"]
                data.append(row)

            df = pd.DataFrame(data=data)
            df["D_TXT"] = df["D_TXT"].str.replace("-99", "1970-01-01T00:00:00+08:00")
            df["D_TNT"] = df["D_TNT"].str.replace("-99", "1970-01-01T00:00:00+08:00")
            df["WDIR"] = df["WDIR"].replace({"-99": np.nan})
            df["WDIR"] = df["WDSD"].replace({"-99": np.nan})
            df["TEMP"] = df["TEMP"].replace({"-99": np.nan})
            df["HUMD"] = df["HUMD"].replace({"-99": np.nan})
            df = df.astype(self._df_astype)
            row_count, col_count = df.shape
            self._df = df
            self._metadata = {"row_count": row_count, "col_count": col_count}

    @property
    def df(self) -> pd.DataFrame:
        return self._df

    @property
    def metadata(self) -> Dict:
        return self._metadata


@dataclass
class BronzeRainConditionTable(BronzeWeatherTableBase):
    def __post_init__(self) -> None:
        self._df_astype = {
            "lat": "float32",
            "lon": "float32",
            "locationName": "str",
            "stationId": "str",
            "CITY": "str",
            "CITY_SN": "str",
            "TOWN": "str",
            "TOWN_SN": "str",
            "obsTime": "datetime64[ns, Asia/Taipei]",
            "ELEV": "float32",
            "RAIN": "float32",
            "MIN_10": "float32",
            "HOUR_3": "float32",
            "HOUR_6": "float32",
            "HOUR_12": "float32",
            "HOUR_24": "float32",
            "NOW": "float32",
            "latest_2days": "float32",
            "latest_3days": "float32",
        }

    def discover(self) -> None:
        data: List[Dict[str, str]] = []
        try:
            json_obj = orjson.loads(self._raw_contents)
        except orjson.JSONEncodeError as e:
            raise e
        else:
            locations = json_obj.get("records").get("location")
            for location in locations:
                row = {
                    "lat": location["lat"],
                    "lon": location["lon"],
                    "locationName": location["locationName"],
                    "stationId": location["stationId"],
                    "obsTime": location["time"]["obsTime"],
                }
                for item in location["weatherElement"]:
                    row[item["elementName"]] = item["elementValue"]
                for item in location["parameter"]:
                    row[item["parameterName"]] = item["parameterValue"]
                data.append(row)

            df = pd.DataFrame(data=data)
            df = df.astype(self._df_astype)
            row_count, col_count = df.shape
            self._df = df
            self._metadata = {"row_count": row_count, "col_count": col_count}

    @property
    def df(self) -> pd.DataFrame:
        return self._df

    @property
    def metadata(self) -> Dict:
        return self._metadata
