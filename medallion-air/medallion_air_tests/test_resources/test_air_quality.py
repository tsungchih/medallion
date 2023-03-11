import os

import pytest
from dagster import InitResourceContext, build_init_resource_context

from medallion_air.resources.gcs_client import GCSClient, gcs_client


@pytest.mark.parametrize(
    "project_id, credentials",
    [(os.environ.get("GOOGLE_CLOUD_PROJECT"), os.environ.get("GOOGLE_APPLICATION_DEFAULT"))],
)
def test_resources__init_gcs_client(project_id: str, credentials: str):
    ctx: InitResourceContext = build_init_resource_context(
        config={"project_id": project_id, "credentials": credentials}
    )
    client = gcs_client(ctx)

    assert isinstance(client, GCSClient)


def test_resources__gcs_client_download_blob_as_bytes():
    ctx: InitResourceContext = build_init_resource_context()
    client: GCSClient = gcs_client(ctx)
    res = client.download_blob_as_bytes(
        bucket_name="bucket-for-pub-dataset",
        blob_name="yellow_tripdata_sample/year=2019/month=1/yellow_tripdata_sample_2019-01.csv",
    )

    assert len(res) > 0


def test_resources__gcs_client_download_blob_as_str():
    ctx: InitResourceContext = build_init_resource_context()
    client: GCSClient = gcs_client(ctx)
    res = client.download_blob_as_str(
        bucket_name="bucket-for-pub-dataset",
        blob_name="yellow_tripdata_sample/year=2019/month=1/yellow_tripdata_sample_2019-01.csv",
    )

    assert len(res) > 0
