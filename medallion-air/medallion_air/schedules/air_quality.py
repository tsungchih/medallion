from dagster import (
    DefaultScheduleStatus,
    RunRequest,
    ScheduleEvaluationContext,
    build_schedule_from_partitioned_job,
    schedule,
)

from ..jobs.air_quality import all_air_assets_job, all_air_assets_partitioned_job
from ..jobs.job_clean import job_clean

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
    run_config = {
        "ops": {
            "bronze_aqi_asset": {"config": {"api_uri": {"env": "MEDALLION_AIR_AQI_URI"}}},
            "bronze_pm10_asset": {"config": {"api_uri": {"env": "MEDALLION_AIR_PM10_URI"}}},
            "bronze_pm25_asset": {"config": {"api_uri": {"env": "MEDALLION_AIR_PM25_URI"}}},
        }
    }
    return RunRequest(run_config=run_config, tags={"scheduled_date": scheduled_date})


@schedule(
    cron_schedule="0/3 * * * *",
    job=job_clean,
    tags=schedule_tags,
    execution_timezone="Asia/Taipei",
    default_status=DefaultScheduleStatus.RUNNING,
)
def hourly_job_clean_schedule(_context: ScheduleEvaluationContext):
    """This schedule execute `job_clean` every hour.

    Args:
        _context (ScheduleEvaluationContext): The schedule evaluation context.

    Returns:
        RunRequest: The corresponding run request object.
    """
    run_config = {
        "ops": {
            "get_concerned_job_runs": {
                "config": {
                    "job_name": "*",
                    "retention": {
                        "purge_after_days": {
                            "canceled": {"env": "MEDALLION_AIR_PURGE_CANCELED_JOBS_AFTER_DAYS"},
                            "failure": {"env": "MEDALLION_AIR_PURGE_FAILURE_JOBS_AFTER_DAYS"},
                            "success": {"env": "MEDALLION_AIR_PURGE_SUCCESS_JOBS_AFTER_DAYS"},
                        }
                    },
                }
            },
        }
    }
    yield RunRequest(run_key=None, run_config=run_config)
