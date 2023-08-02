from dagster import AssetSelection, define_asset_job

from medallion_weather.assets import ALL_ASSET_GROUPS
from medallion_weather.assets.partitions import hourly_partitions_def
from medallion_weather.resources.configs import define_all_assets_job_run_config

DAGSTER_K8S_CONFIG_TAGS = {
    "dagster-k8s/config": {
        "container_config": {
            "resources": {
                "requests": {"cpu": "1000m", "memory": "2Gi"},
                "limits": {"cpu": "1000m", "memory": "2Gi"},
            }
        }
    }
}

DAGSTER_JOB_RETRY_TAGS = {
    "dagster/max-retries": 3,
    "dagster/retry-strategy": "ALL_STEPS",
}

all_assets_job = define_asset_job(
    name="all_assets_job",
    config=define_all_assets_job_run_config(),
    selection=AssetSelection.groups(*ALL_ASSET_GROUPS),
    description="This job tries to materialize all asset groups.",
    tags={**DAGSTER_K8S_CONFIG_TAGS},
    partitions_def=hourly_partitions_def,
)
