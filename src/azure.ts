import { logger } from "./logging";

const AZURE_BLOB_ACCOUNT_NAME = process.env.AZURE_BLOB_ACCOUNT_NAME;
const AZURE_BLOB_SAS = process.env.AZURE_BLOB_SAS;

if (!AZURE_BLOB_ACCOUNT_NAME || !AZURE_BLOB_SAS) {
    logger.error("Azure environment variables not set");
    throw new Error("Azure environment variables not set");
}

export class AzureStorage {
    private urlTemplate: string;

    constructor() {
        this.urlTemplate = `https://${AZURE_BLOB_ACCOUNT_NAME}.blob.core.windows.net/{container}/{blob}?${AZURE_BLOB_SAS}`;
    }

    async putBlob(
        containerName: string,
        blobName: string,
        content: string | Buffer
    ) {
        const url = this.urlTemplate
            .replace("{container}", containerName)
            .replace("{blob}", blobName);
        const headers = new Headers({
            "Content-Type": "application/octet-stream",
            "x-ms-date": new Date().toUTCString(),
        });
        const body = content instanceof Buffer ? content : Buffer.from(content);

        return await fetch(url, {
            method: "PUT",
            headers: headers,
            body: body,
        }).then((response) => {
            if (!response.ok) {
                logger.error(`Failed to create blob: ${response.statusText}`);
            }
        });
    }

    async readBlob(containerName: string, blobName: string) {
        const url = this.urlTemplate
            .replace("{container}", containerName)
            .replace("{blob}", blobName);
        const headers = new Headers({
            "Content-Type": "application/octet-stream",
            "x-ms-date": new Date().toUTCString(),
        });

        return await fetch(url, {
            method: "GET",
            headers: headers,
        })
            .then((response) => {
                if (!response.ok) {
                    logger.error(`Failed to read blob: ${response.statusText}`);
                    throw new Error(
                        `Failed to read blob: ${response.statusText}`
                    );
                }
                return response;
            })
            .then(async (response) => await response.blob())
            .then((blob) => {
                return new Response(blob);
            })
            .catch((error) => {
                logger.error(`Failed to read blob: ${error}`);
                return new Response(null, { status: 500 });
            });
    }
}
