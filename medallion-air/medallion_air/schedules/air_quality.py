from dagster import (
    DefaultScheduleStatus,
    EnvVar,
    RunConfig,
    RunRequest,
    ScheduleEvaluationContext,
    build_schedule_from_partitioned_job,
    schedule,
)

from ..jobs.air_quality import all_air_assets_job, all_air_assets_partitioned_job
from ..jobs.job_clean import job_clean
from ..resources.configs import (
    ApiConfig,
    JobCleanOpConfig,
    PurgeAfterDaysResourceConfig,
    RetentionResourceConfig,
)

schedule_tags = {"module": __name__.split(".")[0], "type": "asset_schedule", "freq": "hourly"}

partitioned_all_assets_schedule = build_schedule_from_partitioned_job(
    job=all_air_assets_partitioned_job,
    name="hourly_partitioned_all_assets_schedule",
    description="The schedule for partitioned asset job.",
    default_status=DefaultScheduleStatus.RUNNING,
)


@schedule(
    cron_schedule="@hourly",
    job=all_air_assets_job,
    tags=schedule_tags,
    execution_timezone="Asia/Taipei",
)
def hourly_all_assets_schedule(_context: ScheduleEvaluationContext):
    scheduled_date = _context.scheduled_execution_time.strftime("%Y-%m-%d")
    ops_config = {
        "bronze_aqi_asset": ApiConfig(api_uri=EnvVar("MEDALLION_AIR_AQI_URI")),
        "bronze_pm10_asset": ApiConfig(api_uri=EnvVar("MEDALLION_AIR_PM10_URI")),
        "bronze_pm25_asset": ApiConfig(api_uri=EnvVar("MEDALLION_AIR_PM25_URI")),
    }
    run_config = RunConfig(ops=ops_config)
    return RunRequest(run_config=run_config, tags={"scheduled_date": scheduled_date})


@schedule(
    cron_schedule="0/30 * * * *",
    job=job_clean,
    tags=schedule_tags,
    execution_timezone="Asia/Taipei",
    default_status=DefaultScheduleStatus.STOPPED,
)
def hourly_job_clean_schedule(_context: ScheduleEvaluationContext):
    """This schedule execute `job_clean` every hour.

    Args:
        _context (ScheduleEvaluationContext): The schedule evaluation context.

    Returns:
        RunRequest: The corresponding run request object.
    """
    ops_config = {
        "get_concerned_job_runs": JobCleanOpConfig(
            job_name="*",
            retention=RetentionResourceConfig(
                purge_after_days=PurgeAfterDaysResourceConfig(success=-1, failure=-1, canceled=-1)
            ),
        )
    }
    run_config = RunConfig(ops=ops_config)
    yield RunRequest(run_key=None, run_config=run_config)
