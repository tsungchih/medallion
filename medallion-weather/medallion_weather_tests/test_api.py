import os

import orjson
import pytest
import requests


@pytest.mark.parametrize(
    "api_uri",
    [os.environ.get("MEDALLION_WEATHER_WEATHER_URI"), os.environ.get("MEDALLION_WEATHER_RAIN_URI")],
)
def test_api__get_weather_uri(api_uri: str):
    raw_data = requests.get(api_uri).text

    json_obj = orjson.loads(raw_data)

    assert len(raw_data) > 0
    assert "records" in json_obj
