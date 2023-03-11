from dagster import DagsterRunStatus, Field, IntSource, Noneable, StringSource


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
