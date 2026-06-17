import { GetObjectCommand, PutObjectCommand, S3Client, HeadObjectCommand } from "@aws-sdk/client-s3";
import { mkdir, readFile, writeFile } from "node:fs/promises";
import path from "node:path";

export type ObjectStorageBucket = "corpus-assets" | "tts-audio";

export interface StoredObject {
  bucket: ObjectStorageBucket;
  key: string;
  contentType: string;
  publicUrl?: string;
  etag?: string;
}

export interface PutObjectRequest {
  bucket: ObjectStorageBucket;
  key: string;
  contentType: string;
  body: Uint8Array;
}

export interface GetObjectRequest {
  bucket: ObjectStorageBucket;
  key: string;
}

export interface ObjectStorageClient {
  putObject(request: PutObjectRequest): Promise<StoredObject>;
  getObject(request: GetObjectRequest): Promise<Uint8Array>;
  getPublicUrl(request: GetObjectRequest): string;
  exists(request: GetObjectRequest): Promise<boolean>;
}

export interface S3ObjectStorageConfig {
  region: string;
  endpoint?: string;
  forcePathStyle?: boolean;
  buckets: Record<ObjectStorageBucket, string>;
  publicBaseUrls?: Partial<Record<ObjectStorageBucket, string>>;
}

export function createS3ObjectStorageClient(config: S3ObjectStorageConfig): ObjectStorageClient {
  const client = new S3Client({
    region: config.region,
    endpoint: config.endpoint,
    forcePathStyle: config.forcePathStyle
  });

  return {
    async putObject(request) {
      const bucket = config.buckets[request.bucket];
      const result = await client.send(
        new PutObjectCommand({
          Bucket: bucket,
          Key: request.key,
          Body: request.body,
          ContentType: request.contentType
        })
      );

      return {
        bucket: request.bucket,
        key: request.key,
        contentType: request.contentType,
        publicUrl: this.getPublicUrl(request),
        etag: result.ETag
      };
    },

    async getObject(request) {
      const bucket = config.buckets[request.bucket];
      const result = await client.send(
        new GetObjectCommand({
          Bucket: bucket,
          Key: request.key
        })
      );

      if (!result.Body) {
        throw new Error(`Object ${request.bucket}/${request.key} returned an empty body.`);
      }

      return result.Body.transformToByteArray();
    },

    async exists(request) {
      const bucket = config.buckets[request.bucket];
      try {
        await client.send(
          new HeadObjectCommand({
            Bucket: bucket,
            Key: request.key
          })
        );
        return true;
      } catch (err: any) {
        if (err.name === "NotFound" || err.$metadata?.httpStatusCode === 404) {
          return false;
        }
        throw err;
      }
    },

    getPublicUrl(request) {
      const baseUrl = config.publicBaseUrls?.[request.bucket];

      if (!baseUrl) {
        throw new Error(`No public base URL configured for bucket ${request.bucket}.`);
      }

      return `${baseUrl.replace(/\/$/, "")}/${encodePathSegments(request.key)}`;
    }
  };
}

export interface LocalObjectStorageConfig {
  rootDir: string;
  publicBaseUrl: string;
}

export function createLocalObjectStorageClient(config: LocalObjectStorageConfig): ObjectStorageClient {
  return {
    async putObject(request) {
      const targetPath = getLocalObjectPath(config.rootDir, request);
      await mkdir(path.dirname(targetPath), { recursive: true });
      await writeFile(targetPath, request.body);

      return {
        bucket: request.bucket,
        key: request.key,
        contentType: request.contentType,
        publicUrl: this.getPublicUrl(request)
      };
    },

    async getObject(request) {
      return readFile(getLocalObjectPath(config.rootDir, request));
    },

    async exists(request) {
      try {
        await import("node:fs/promises").then(fs => fs.stat(getLocalObjectPath(config.rootDir, request)));
        return true;
      } catch (err: any) {
        if (err.code === "ENOENT") return false;
        throw err;
      }
    },

    getPublicUrl(request) {
      return `${config.publicBaseUrl.replace(/\/$/, "")}/${request.bucket}/${encodePathSegments(request.key)}`;
    }
  };
}

export function buildCorpusAssetKey(lessonId: string, assetName: string): string {
  return `lessons/${lessonId}/assets/${assetName}`;
}

export function buildTtsAudioKey(lessonId: string, voiceId: string, contentHash: string): string {
  return `lessons/${lessonId}/tts/${voiceId}/${contentHash}.mp3`;
}

function getLocalObjectPath(rootDir: string, request: GetObjectRequest): string {
  return path.join(rootDir, request.bucket, ...request.key.split("/"));
}

function encodePathSegments(key: string): string {
  return key.split("/").map(encodeURIComponent).join("/");
}
