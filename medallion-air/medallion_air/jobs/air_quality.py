from dagster import AssetSelection, JobDefinition, define_asset_job

from medallion_air.assets import (
    bronze_layer_assets,
    gold_layer_assets,
    silver_layer_assets,
)
from medallion_air.assets.partitions import hourly_partitions_def
from medallion_air.jobs import JOB_RETRY_TAGS

_dagster_k8s_tags = {
    "dagster-k8s/config": {
        "container_config": {
            "resources": {
                "requests": {"cpu": "250m", "memory": "256Mi"},
                "limits": {"cpu": "1000m", "memory": "1024Mi"},
            },
        }
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
    partitions_def=hourly_partitions_def,
    tags={**_dagster_k8s_tags, **_job_tags, **JOB_RETRY_TAGS},
)
