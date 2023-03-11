from dagster import DagsterRunStatus, job

from medallion_air.jobs import JOB_RETRY_TAGS

from ..ops import (
    delete_job_runs,
    get_concerned_job_runs,
    get_op_filter_job_runs_with_status,
)

filter_failure_job_runs = get_op_filter_job_runs_with_status(status=DagsterRunStatus.FAILURE)
filter_success_job_runs = get_op_filter_job_runs_with_status(status=DagsterRunStatus.SUCCESS)
filter_canceled_job_runs = get_op_filter_job_runs_with_status(status=DagsterRunStatus.CANCELED)


@job(tags={**JOB_RETRY_TAGS})
def job_clean():
    """This job cleans job with status of SUCCESS"""
    concerned_job_runs = get_concerned_job_runs()
    success_job_run_ids = filter_success_job_runs(concerned_job_runs)
    failure_job_run_ids = filter_failure_job_runs(concerned_job_runs)
    canceled_job_run_ids = filter_canceled_job_runs(concerned_job_runs)
    delete_job_runs(success_job_run_ids, failure_job_run_ids, canceled_job_run_ids)
