import os

import pytest

from medallion_weather.schemas.factory import WeatherTableFactory
from medallion_weather.schemas.weather_tables import (
    BronzeRainConditionTable,
    BronzeWeatherTable,
)
from medallion_weather.typing import WeatherTableType


def test_factory__returns_same_instance():
    factory1 = WeatherTableFactory()
    factory2 = WeatherTableFactory()

    assert factory1 == factory2


def test_factory__returns_correct_object():
    factory = WeatherTableFactory()
    obj1 = factory.create_object(otype=WeatherTableType.WEATHER, contents="")
    obj2 = factory.create_object(otype=WeatherTableType.RAIN, contents="")

    assert isinstance(obj1, BronzeWeatherTable)
    assert isinstance(obj2, BronzeRainConditionTable)


@pytest.mark.parametrize(
    "table_type, file_name",
    [(WeatherTableType.WEATHER, "weather.json"), (WeatherTableType.RAIN, "rain.json")],
)
def test_table__weather_table(table_type, file_name):
    factory = WeatherTableFactory()
    dirname = os.path.dirname(__file__)
    fpath = os.path.join(dirname, "test-data", file_name)
    with open(fpath, "r") as f:
        fcontents = f.read()
        table_obj = factory.create_object(otype=table_type, contents=fcontents)
        table_obj.discover()
    assert table_obj.df.shape[0] > 0
    assert table_obj.metadata is not None
