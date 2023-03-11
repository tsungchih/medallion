import os

import orjson
import pytest
import requests
from dotenv import load_dotenv

load_dotenv()


# @pytest.mark.parametrize(
#     "api_uri",
#     [
#         os.environ.get("MEDALLION_AIR_PM25_URI"),
#         os.environ.get("MEDALLION_AIR_PM10_URI"),
#         os.environ.get("MEDALLION_AIR_AQI_URI"),
#     ],
# )
# def test_apis(api_uri: str):
#     assert api_uri is not None

#     raw_json: str = requests.get(api_uri).text
#     assert "records" in raw_json
