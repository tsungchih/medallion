from datetime import datetime, timedelta
from typing import List, Optional, Sequence

import dagster._check as check
from dagster import (
    DagsterInstance,
    DagsterRun,
    DagsterRunStatus,
    OpExecutionContext,
    RunRecord,
    RunsFilter,
    op,
)

from ..resources.configs import define_job_clean_config_schema


def get_op_filter_job_runs_with_status(status: DagsterRunStatus, job_name: Optional[str] = None):
    status_str = status.value.lower()
    name = job_name or f"filter_job_runs_with_status_{status_str}"

    @op(name=name)
    def filter_job_runs_with_status(
        context: OpExecutionContext, results: List[DagsterRun]
    ) -> List[str]:
        """This op filters out job runs that has a given status.

        Args:
            context (OpExecutionContext): The Op execution context.
            results: A list of query results derived from Dagster Instance.

        Returns:
            List[str]: A list of `runId` having the given status.
        """
        job_runs_list = [run.run_id for run in results if run.status == status]
        context.log.info(job_runs_list)
        return job_runs_list

    return filter_job_runs_with_status


@op(config_schema=define_job_clean_config_schema())
def get_concerned_job_runs(context: OpExecutionContext):
    """This op filtered out the list of specified status of the given job.

    Args:
        context (OpExecutionContext): The Op execution context.
    """
    job_name = context.op_config.get("job_name") or "*"
    retention_info = context.op_config["retention"]
    purge_after_days = retention_info["purge_after_days"]
    check.str_param(job_name, "job_name")
    check.dict_param(
        obj=purge_after_days, param_name="purge_after_days", key_type=str, value_type=int
    )
    dagster_instance: DagsterInstance = context.instance
    concerned_status: List[str] = [
        status_value for status_value in purge_after_days if purge_after_days[status_value] >= 0
    ]

    datetime_now = datetime.now()
    results: List[DagsterRun] = []

    for run_status in concerned_status:
        updated_before_timestamp = datetime_now - timedelta(days=purge_after_days[run_status])
        job_runs_filter = RunsFilter(
            job_name=job_name if not job_name == "*" else None,
            statuses=[DagsterRunStatus(run_status.upper())],
            updated_before=updated_before_timestamp,
        )
        matched_runs: Sequence[RunRecord] = dagster_instance.get_run_records(
            filters=job_runs_filter
        )
        results += [run.dagster_run for run in matched_runs]
    context.log.info(f"Number of results: {len(results)}")

    return results


@op
def delete_job_runs(
    context: OpExecutionContext,
    success_run_id: List[str],
    failure_run_id: List[str],
    canceled_run_id: List[str],
):
    """This op deletes pipeline runs according to the given list of run IDs.

    Args:
        context (OpExecutionContext): The Op execution context.
        run_id (List[str]): The list of run IDs to be deleted.
    """
    dagster_instance: DagsterInstance = context.instance
    run_id = success_run_id + failure_run_id + canceled_run_id
    for id in run_id:
        dagster_instance.delete_run(run_id=id)
