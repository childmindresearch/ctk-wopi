"""Entrypoint for the Azure Functions app."""

import http
import json

from azure import functions

from ctk_wopi import azure, config

logger = config.get_logger()

app = functions.FunctionApp()


@app.function_name(name="GetFileMetaData")
@app.route(
    route="wopi/files/{name}",
    auth_level=functions.AuthLevel.FUNCTION,
    methods=["GET"],
)
async def get_file_metadata(req: functions.HttpRequest) -> functions.HttpResponse:
    """Fetches the metadata of a file from Azure Blob Storage.

    Args:
        req: The HTTP request object.

    Returns:
        The HTTP response containing the file metadata
    """
    name = req.route_params.get("name", None)
    logger.info("Fetching file metadata for %s.", name)
    client = azure.AzureBlobStorage()
    metadata = client.read_blob_metadata("templates", name)
    file_size = metadata.get("size", 0)
    response = json.dumps(
        {
            "BaseFileName": name,
            "OwnerId": 1000,
            "UserId": 1000,
            "Size": file_size,
            "UserCanWrite": True,
        },
    )
    return functions.HttpResponse(
        body=response,
        status_code=http.HTTPStatus.OK,
        mimetype="application/json",
    )


@app.function_name(name="GetFileContents")
@app.route(
    route="wopi/files/{name}/contents",
    auth_level=functions.AuthLevel.FUNCTION,
    methods=["GET"],
)
async def get_file_contents(req: functions.HttpRequest) -> functions.HttpResponse:
    """Fetches the metadata of a file from Azure Blob Storage.

    Args:
        req: The HTTP request object.

    Returns:
        The HTTP response containing the file metadata
    """
    name = req.route_params.get("name", None)
    logger.info("Fetching file contents for %s.", name)
    client = azure.AzureBlobStorage()
    metadata = client.read_blob("templates", name)
    return functions.HttpResponse(
        body=metadata,
        status_code=http.HTTPStatus.OK,
        mimetype="application/octet-stream",
    )


@app.function_name(name="PutFileContents")
@app.route(
    route="wopi/files/{name}/contents",
    auth_level=functions.AuthLevel.FUNCTION,
    methods=["PUT"],
)
async def put_file_contents(req: functions.HttpRequest) -> functions.HttpResponse:
    """Fetches the metadata of a file from Azure Blob Storage.

    Args:
        req: The HTTP request object.

    Returns:
        The HTTP response containing the file metadata
    """
    name = req.route_params.get("name", None)
    logger.info("Updating file contents for %s.", name)
    contents = req.get_body()
    client = azure.AzureBlobStorage()
    client.update_blob("templates", name, contents)
    return functions.HttpResponse("", status_code=http.HTTPStatus.CREATED)
