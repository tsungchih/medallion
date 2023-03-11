from dataclasses import dataclass
from typing import List, Optional

import google.auth
from dagster import InitResourceContext, StringSource, resource
from google.cloud import storage
from google.cloud.storage.bucket import Blob, Bucket


@dataclass
class GCSClient(object):
    _project_id: str
    _credentials: str

    def __post_init__(self):
        creds, _ = google.auth.load_credentials_from_file(filename=self._credentials)
        self._client = storage.Client(project=self._project_id, credentials=creds)

    def download_blob_as_bytes(self, bucket_name: str, blob_name: str) -> bytes:
        """Download and return the given blob as bytes.

        Given the `bucket_name` and the `blob_name`, this function downloads and returns the blob
        as bytes.

        Args:
            bucket_name (str): The bucket name on GCS.
            blob_name (str): The blob name on GCS.

        Returns:
            bytes: The blob contents with bytes.
        """
        bucket: Bucket = self._client.bucket(bucket_name)
        blob: Blob = bucket.blob(blob_name)
        res = blob.download_as_bytes(self._client)

        return res

    def download_blob_as_str(
        self, bucket_name: str, blob_name: str, codec: Optional[str] = "utf-8"
    ) -> str:
        """Download and return the given blob as a string.

        Given the `bucket_name` and the `blob_name`, this function downloads and returns the blob
        as string in terms of the given codec.

        Args:
            bucket_name (str): The bucket name on GCS.
            blob_name (str): The blob name on GCS.
            codec (str): The codec used to decode the bytes contents of the blob.

        Returns:
            str: The blob contents with decoded string.
        """
        res = self.download_blob_as_bytes(bucket_name, blob_name).decode(codec)

        return res

    def list_file_blobs_as_str(
        self,
        bucket_name: str,
        prefix: Optional[str] = None,
        max_results: Optional[int] = None,
        start_offset: Optional[str] = None,
    ) -> List[str]:
        """Returns a list of blob names.

        Args:
            bucket_name (str): The bucket name.
            prefix (Optional[str], optional): Prefix used to filter blobs. Defaults to None.
            max_results (Optional[int], optional): The maximum number of blobs to return.
                Defaults to None.
            start_offset (Optional[str], optional): Filter results to objects whose names are
                lexicographically equal to or after startOffset. If endOffset is also set, the
                objects listed will have names between startOffset (inclusive) and endOffset
                (exclusive). Defaults to None.
            end_offset (Optional[str], optional): Filter results to objects whose names are
                lexicographically before endOffset. If startOffset is also set, the objects
                listed will have names between startOffset (inclusive) and endOffset (exclusive).

        Returns:
            List[str]: _description_
        """
        blob_list = self._client.list_blobs(
            bucket_or_name=bucket_name,
            prefix=prefix,
            max_results=max_results,
            start_offset=start_offset,
        )
        blob_names = [blob.name for blob in blob_list if blob.name.split("/")[-1]]
        return blob_names


@resource(
    config_schema={
        "project_id": StringSource,
        "credentials": StringSource,
    },
    description="The GCS client resource.",
)
def gcs_client(context: InitResourceContext) -> GCSClient:
    project_id = context.resource_config["project_id"]
    credentials = context.resource_config["credentials"]

    return GCSClient(project_id, credentials)
