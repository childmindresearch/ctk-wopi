FROM node:22-alpine as builder

WORKDIR /app

COPY tsconfig.json package.json package-lock.json ./
COPY src /app/src

RUN npm ci; npm run build

FROM node:22-alpine

ENV AZURE_BLOB_ACCOUNT_NAME=""
ENV AZURE_BLOB_SAS=""

EXPOSE 3000

WORKDIR /app

COPY --from=builder /app/package.json /app/package-lock.json ./
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/dist ./dist

CMD ["node", "dist/server.js"]


