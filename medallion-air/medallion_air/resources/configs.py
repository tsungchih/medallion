from datetime import datetime

import pendulum

from dagster import (
    Config,
    DagsterRunStatus,
    EnvVar,
    Field,
    IntSource,
    Noneable,
    RunConfig,
    StringSource,
    hourly_partitioned_config,
)
from medallion_air.assets.partitions import hourly_partitions_def


class AirAPIOpConfig(Config):
    api_uri: str


def job_retention_resource_config_schema():
    days = Field(
        Noneable(IntSource),
        default_value=-1,
        description="""How many days job runs with a given status can be removed. A value of"""
        """-1 indicates that job runs with a given status should be retained indefinitely.""",
    )

    return {
        "retention": {
            "purge_after_days": {
                DagsterRunStatus.SUCCESS.value.lower(): days,
                DagsterRunStatus.FAILURE.value.lower(): days,
                DagsterRunStatus.CANCELED.value.lower(): days,
            }
        }
    }


def define_job_clean_config_schema():
    job_name = Field(
        StringSource, description="The job name to be filtered and cleaned.", is_required=True
    )
    config_schema = {
        "job_name": job_name,
        **job_retention_resource_config_schema(),
    }
    return config_schema


@hourly_partitioned_config(
    start_date=hourly_partitions_def.get_first_partition_window(datetime.now()).start,
    timezone="Asia/Taipei",
)
def partitioned_all_air_assets_job_config(start: datetime, _end: datetime):
    op_config = {
        "bronze_aqi_asset": AirAPIOpConfig(api_uri=EnvVar("MEDALLION_AIR_AQI_URI")),
        "bronze_pm10_asset": AirAPIOpConfig(api_uri=EnvVar("MEDALLION_AIR_PM10_URI")),
        "bronze_pm25_asset": AirAPIOpConfig(api_uri=EnvVar("MEDALLION_AIR_PM25_URI")),
    }

    return RunConfig(ops=op_config).to_config_dict()
