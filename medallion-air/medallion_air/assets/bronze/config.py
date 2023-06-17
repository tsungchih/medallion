from pydantic import Field

from dagster import Config


class ApiConfig(Config):
    api_uri: str = Field(
        ...,
        description="the URL for getting the raw data.",
    )
