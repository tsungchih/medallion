import re
from abc import ABC, abstractmethod
from traceback import print_stack
from typing import Dict

import orjson
import pandas as pd


class AirQualityTableBase(ABC):
    """Base class of air quality related tables."""

    _contents: str = None
    _df: pd.DataFrame = None
    _metadata: Dict = None

    def __init__(self, contents: str) -> None:
        """Initialize AirQualityTableBase.

        Args:
            contents (str): A string conforms to JSON format.
        """
        self._contents = contents

    @abstractmethod
    def discover(self) -> None:
        """Discover DataFrame and metadata from the `self._contentx`."""
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


class BronzePm25Table(AirQualityTableBase):
    """Class of PM25Table."""

    def __init__(self, contents: str) -> None:
        self._df_astype = {
            "pm25": "float32",
            "datacreationdate": "datetime64[ns]",
        }
        refined_contents = re.sub(r'(?:"x"|"-")', '""', contents)
        super().__init__(refined_contents)

    @property
    def df(self) -> pd.DataFrame:
        return self._df

    @property
    def metadata(self) -> Dict:
        return self._metadata

    def discover(self):
        try:
            json_obj = orjson.loads(self._contents)
        except orjson.JSONEncodeError as e:
            print_stack(e)
        else:
            records = json_obj.get("records")
            df = pd.DataFrame(data=records)
            df = df.replace(r"^\s*$", "0", regex=True)
            df = df.astype(self._df_astype)
            row_count, col_count = df.shape
            self._df = df
            self._metadata = {"row_count": row_count, "col_count": col_count}


class BronzePm10Table(AirQualityTableBase):
    """Class of PM10Table."""

    def __init__(self, contents: str) -> None:
        self._df_astype = {
            "itemid": "int8",
            "siteid": "int8",
            "concentration": "float32",
            "monitordate": "datetime64[ns]",
        }
        refined_contents = re.sub(r'(?:"x"|"-")', '""', contents)
        super().__init__(refined_contents)

    @property
    def df(self) -> pd.DataFrame:
        return self._df

    @property
    def metadata(self) -> Dict:
        return self._metadata

    def discover(self):
        try:
            json_obj = orjson.loads(self._contents)
        except orjson.JSONEncodeError as e:
            print_stack(e)
        else:
            records = json_obj.get("records")
            df = pd.DataFrame(data=records)
            df = df.replace(r"^\s*$", "0", regex=True)
            df = df.astype(self._df_astype)
            row_count, col_count = df.shape
            self._df = df
            self._metadata = {"row_count": row_count, "col_count": col_count}


class BronzeAqiTable(AirQualityTableBase):
    """Class of PM10Table."""

    def __init__(self, contents: str) -> None:
        self._df_astype = {
            "publishtime": "datetime64[ns]",
            "wind_direc": "int8",
            "siteid": "int8",
            "longitude": "float32",
            "latitude": "float32",
            "aqi": "float32",
            "so2": "float32",
            "co": "float32",
            "o3": "float32",
            "o3_8hr": "float32",
            "pm10": "float32",
            "pm25": "float32",
            "no2": "float32",
            "nox": "float32",
            "no": "float32",
            "wind_speed": "float32",
            "co_8hr": "float32",
            "pm25_avg": "float32",
            "pm10_avg": "float32",
            "so2_avg": "float32",
        }
        refined_contents = re.sub(r'(?:"x"|"-")', '""', contents)
        super().__init__(refined_contents)

    @property
    def df(self) -> pd.DataFrame:
        return self._df

    @property
    def metadata(self) -> Dict:
        return self._metadata

    def discover(self):
        try:
            json_obj = orjson.loads(self._contents)
        except orjson.JSONEncodeError as e:
            print_stack(e)
        else:
            records = json_obj.get("records")
            df = pd.DataFrame(data=records)
            df.rename(
                columns={
                    "pm2.5": "pm25",
                    "pm2.5_avg": "pm25_avg",
                },
                inplace=True,
            )
            df = df.replace(r"^\s*$", "0", regex=True)
            df = df.astype(self._df_astype)
            row_count, col_count = df.shape
            self._df = df
            self._metadata = {"row_count": row_count, "col_count": col_count}
