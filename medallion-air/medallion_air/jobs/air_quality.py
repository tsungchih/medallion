from dagster import (
    AssetSelection,
    JobDefinition,
    define_asset_job,
    multi_or_in_process_executor,
)
from medallion_air.assets.partitions import hourly_partitions_def
from medallion_air.jobs import JOB_RETRY_TAGS
from medallion_air.resources.configs import partitioned_all_air_assets_job_config

_dagster_k8s_tags = {
    "dagster-k8s/config": {
        "container_config": {
            "resources": {
                "requests": {"cpu": "250m", "memory": "256Mi"},
                "limits": {"cpu": "1000m", "memory": "1024Mi"},
            },
        },
        "job_spec_config": {"ttl_seconds_after_finished": 180},
    }
}

_job_tags = {
    "module": __name__.split(".")[0],
    "type": "asset_job",
}

_all_assets = AssetSelection.groups("bronze", "silver", "gold")


all_air_assets_job: JobDefinition = define_asset_job(
    name="all_air_assets_job",
    selection=_all_assets,
    description="This job materializes all the asstes defined in `medallion_air` python module.",
    tags={**_dagster_k8s_tags, **_job_tags, **JOB_RETRY_TAGS},
)

all_air_assets_partitioned_job: JobDefinition = define_asset_job(
    name="all_air_assets_partitioned_job",
    selection=_all_assets,
    description="This job materializes all the asstes.",
    executor_def=multi_or_in_process_executor,
    partitions_def=hourly_partitions_def,
    tags={**_dagster_k8s_tags, **_job_tags, **JOB_RETRY_TAGS},
    config=partitioned_all_air_assets_job_config,
)
