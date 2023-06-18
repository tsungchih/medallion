from dagster import EnvVar
from dagster_gcp.gcs.io_manager import (
    ConfigurablePickledObjectGCSIOManager,
    GCSResource,
)
from dagster_gcp_pandas import BigQueryPandasIOManager

from .gcs_client import GCSClient

RESOURCES_DEV = {
    "bq_io_manager": BigQueryPandasIOManager(
        project=EnvVar("GOOGLE_CLOUD_PROJECT"), location="us-west1", timeout=10.0
    ),
    "gcs_io_manager": ConfigurablePickledObjectGCSIOManager(
        gcs=GCSResource(), gcs_bucket="dagster-demo-iomanager", gcs_prefix="dagster"
    ),
    "gcs_client": GCSClient(
        project_id=EnvVar("GOOGLE_CLOUD_PROJECT"),
        credentials=EnvVar("GOOGLE_APPLICATION_CREDENTIALS"),
    ),
}

RESOURCES_PROD = {
    "gcs_client": GCSClient(
        project_id=EnvVar("GOOGLE_CLOUD_PROJECT"),
        credentials=EnvVar("GOOGLE_APPLICATION_CREDENTIALS"),
    ),
}


resource_defs_by_env = {
    "dev": RESOURCES_DEV,
    "prod": RESOURCES_PROD,
}
