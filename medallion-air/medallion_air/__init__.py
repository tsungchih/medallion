import os

from dotenv import load_dotenv

from dagster import Definitions, load_assets_from_modules, multiprocess_executor
from medallion_air import assets

from .jobs.air_quality import all_air_assets_job
from .jobs.job_clean import job_clean
from .resources import resource_defs_by_env
from .schedules.air_quality import (
    hourly_all_assets_schedule,
    hourly_job_clean_schedule,
    partitioned_all_assets_schedule,
)

load_dotenv()
deploy_env = os.environ.get("MEDALLION_AIR_ENV", "dev")

all_assets = load_assets_from_modules(modules=[assets])
all_jobs = [all_air_assets_job, job_clean]
all_schedules = [
    partitioned_all_assets_schedule,
    hourly_all_assets_schedule,
    hourly_job_clean_schedule,
]
resource_defs = resource_defs_by_env[deploy_env]

medallion_air_defs = Definitions(
    assets=all_assets,
    jobs=all_jobs,
    schedules=all_schedules,
    resources=resource_defs,
    executor=multiprocess_executor,
)
