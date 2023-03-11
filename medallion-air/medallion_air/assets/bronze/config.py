import os

from dagster import Config, StringSource
from pydantic import Field


class ApiConfig(Config):
    api_uri: str = Field(
        ...,
        description="the URL for getting the raw data.",
    )
