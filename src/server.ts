import express from "express";
import { logger } from "./logging";
import { AzureStorage } from "./azure";

const app = express();
const PORT = 3000;

app.get(
    "/wopi/files/:name",
    async (req: express.Request, res: express.Response) => {
        const name = decodeURIComponent(req.params.name);
        logger.info(`Retrieving file ${name} from WOPI server.`);

        const response = await new AzureStorage().readBlob("templates", name);

        if (!response.ok) {
            logger.error(`Failed to read blob: ${response.statusText}`);
            res.status(500).send();
            return;
        }
        const filesize = response.headers.get("Content-Length");
        res.json({
            BaseFileName: name,
            Size: filesize,
            OwnerId: 1000,
            UserId: 1000,
            UserCanWrite: true,
        });
    }
);

app.get(
    "/wopi/files/:name/contents",
    async (req: express.Request, res: express.Response) => {
        const name = decodeURIComponent(req.params.name);

        logger.info(`Retrieving file ${name} from WOPI server.`);

        const response = await new AzureStorage().readBlob("templates", name);
        if (!response.body) {
            logger.error("Response body is null");
            res.status(500).send();
            return;
        }
        res.type("docx");
        res.send(Buffer.from(await response.arrayBuffer()));
    }
);

app.put(
    "/wopi/files/:name/contents",
    async (req: express.Request, res: express.Response) => {
        const name: string = decodeURIComponent(req.params.name);

        logger.info(`Saving file ${name} to WOPI server.`);

        await new AzureStorage().putBlob("templates", name, req.body);
        res.send();
    }
);

app.listen(PORT, () => {
    logger.info(`WOPI server listening at http://localhost:${PORT}`);
});
