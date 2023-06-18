from dagster import (
    AssetKey,
    DefaultSensorStatus,
    EnvVar,
    EventLogEntry,
    RunConfig,
    RunRequest,
    SensorEvaluationContext,
    asset_sensor,
)
from dagster_gcp_pandas import BigQueryPandasIOManager

from ..jobs import DAGSTER_K8S_CONFIG_TAGS, all_assets_job
from ..resources.configs import define_all_assets_job_run_config


@asset_sensor(
    asset_key=AssetKey(["GCP", "test_pub_dataset", "gold_aqi_with_pm_asset"]),
    job=all_assets_job,
    default_status=DefaultSensorStatus.STOPPED,
    minimum_interval_seconds=30,
    name="sensor_of_gold_aqi_with_pm_asset",
    description="This is an asset sensor with respect to `gold_aqi_with_pm_asset` from the domain `medallion_air`.",
)
def from_air_gold_aqi_with_pm_asset(_context: SensorEvaluationContext, asset_event: EventLogEntry):
    run_key = _context.cursor
    run_config = define_all_assets_job_run_config()
    run_req: RunRequest = all_assets_job.run_request_for_partition(
        run_key=run_key,
        partition_key=asset_event.dagster_event.partition,
        run_config=run_config,
        tags=DAGSTER_K8S_CONFIG_TAGS,
    )
    _context.update_cursor(run_key)
    yield run_req
