"""Interactions with Azure other services."""

from azure.storage import blob

from ctk_wopi import config

settings = config.get_settings()

AZURE_STORAGE_ACCOUNT_NAME = settings.AZURE_STORAGE_ACCOUNT_NAME
AZURE_STORAGE_SAS = settings.AZURE_STORAGE_SAS


class AzureBlobStorage:
    """Represents a client for interacting with Azure Blob Storage.

    Attributes:
        client: The BlobServiceClient instance used for interacting with the Azure Blob
            Storage.
    """

    def __init__(self) -> None:
        """Initializes a new instance of the AzureBlobStorage class."""
        self.client = blob.BlobServiceClient(
            account_url=f"https://{AZURE_STORAGE_ACCOUNT_NAME.get_secret_value()}.blob.core.windows.net",
            credential=AZURE_STORAGE_SAS.get_secret_value(),
        )

    def read_blob(self, container_name: str, blob_name: str) -> bytes:
        """Reads the contents of a blob from the specified container.

        Args:
            container_name: The name of the container.
            blob_name: The name of the blob.

        Returns:
            The contents of the blob as bytes.
        """
        container_client = self.client.get_container_client(container_name)
        blob_client = container_client.get_blob_client(blob_name)
        return blob_client.download_blob().readall()

    def read_blob_metadata(self, container_name: str, blob_name: str) -> dict:
        """Reads the metadata of a blob from the specified container.

        Args:
            container_name: The name of the container.
            blob_name: The name of the blob.

        Returns:
            The metadata of the blob as a dictionary.
        """
        container_client = self.client.get_container_client(container_name)
        blob_client = container_client.get_blob_client(blob_name)
        return blob_client.get_blob_properties().metadata

    def create_blob(self, container_name: str, blob_name: str, data: bytes) -> None:
        """Creates a new blob in the specified container with the given data.

        Args:
            container_name: The name of the container.
            blob_name: The name of the blob.
            data: The data to be uploaded as bytes.
        """
        container_client = self.client.get_container_client(container_name)
        blob_client = container_client.get_blob_client(blob_name)
        blob_client.upload_blob(data, overwrite=False)

    def update_blob(self, container_name: str, blob_name: str, data: bytes) -> None:
        """Updates an existing blob in the specified container with the given data.

        Args:
            container_name: The name of the container.
            blob_name: The name of the blob.
            data: The data to be uploaded as bytes.
        """
        container_client = self.client.get_container_client(container_name)
        blob_client = container_client.get_blob_client(blob_name)
        blob_client.upload_blob(data, overwrite=True)

    def delete_blob(self, container_name: str, blob_name: str) -> None:
        """Deletes a blob from the specified container.

        Args:
            container_name: The name of the container.
            blob_name: The name of the blob.
        """
        container_client = self.client.get_container_client(container_name)
        blob_client = container_client.get_blob_client(blob_name)
        blob_client.delete_blob()
