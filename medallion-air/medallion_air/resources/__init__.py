from dagster_gcp.gcs import ConfigurablePickledObjectGCSIOManager, GCSResource
from dagster_gcp_pandas import BigQueryPandasIOManager

from dagster import EnvVar

from .gcs_client import GCSClient

RESOURCES_DEV = {
    "gcs_io_manager": ConfigurablePickledObjectGCSIOManager(
        gcs=GCSResource(), gcs_bucket="dagster-demo-iomanager", gcs_prefix="dagster"
    ),
    "gcs_client": GCSClient(
        project_id=EnvVar("GOOGLE_CLOUD_PROJECT"),
        credentials=EnvVar("GOOGLE_APPLICATION_CREDENTIALS"),
    ),
    "bq_io_manager": BigQueryPandasIOManager.configure_at_launch(),
}

RESOURCES_PROD = {
    "gcs_client": GCSClient(
        project_id=EnvVar("GOOGLE_CLOUD_PROJECT"),
        credentials=EnvVar("GOOGLE_APPLICATION_CREDENTIALS"),
    )
}

resource_defs_by_env = {
    "dev": RESOURCES_DEV,
    "prod": RESOURCES_PROD,
}
