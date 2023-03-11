from dagster_gcp.gcs import gcs_pickle_io_manager, gcs_resource

from .gcs_client import gcs_client

RESOURCES_DEV = {
    "gcs_io_manager": gcs_pickle_io_manager.configured(
        {
            "gcs_bucket": "dagster-demo-iomanager",
            "gcs_prefix": "dagster",
        }
    ),
    "gcs": gcs_resource,
    "gcs_client": gcs_client.configured(
        {
            "project_id": {"env": "GOOGLE_CLOUD_PROJECT"},
            "credentials": {"env": "GOOGLE_APPLICATION_CREDENTIALS"},
        }
    ),
}

RESOURCES_PROD = {
    "gcs_client": gcs_client.configured(
        {
            "project_id": {"env": "GOOGLE_CLOUD_PROJECT"},
            "credentials": {"env": "GOOGLE_APPLICATION_CREDENTIALS"},
        }
    )
}


resource_defs_by_env = {
    "dev": RESOURCES_DEV,
    "prod": RESOURCES_PROD,
}
