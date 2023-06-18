from dagster import Config, EnvVar, RunConfig
from dagster_gcp_pandas import BigQueryPandasIOManager
from pydantic import Field


class ApiOpsConfig(Config):
    api_uri: str = Field(
        ...,
        description="The API uri for retrieving JSON format raw data.",
    )


def define_all_assets_job_run_config() -> RunConfig:
    resources_config = {
        "bq_io_manager": BigQueryPandasIOManager(
            project=EnvVar("GOOGLE_CLOUD_PROJECT"),
            location="us-west1",
            timeout=10.0,
        )
    }
    ops_config = {
        "bronze_rain_condition_asset": ApiOpsConfig(api_uri=EnvVar("MEDALLION_WEATHER_RAIN_URI")),
        "bronze_weather_asset": ApiOpsConfig(api_uri=EnvVar("MEDALLION_WEATHER_WEATHER_URI")),
    }
    return RunConfig(ops=ops_config, resources=resources_config)
