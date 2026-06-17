import type { ObjectStorageBucket, S3ObjectStorageConfig } from "./index.js";

export interface ObjectStorageEnv {
  AWS_REGION?: string;
  S3_ENDPOINT?: string;
  S3_FORCE_PATH_STYLE?: string;
  CORPUS_ASSETS_BUCKET?: string;
  TTS_AUDIO_BUCKET?: string;
  CORPUS_ASSETS_PUBLIC_URL?: string;
  TTS_AUDIO_PUBLIC_URL?: string;
}

export function loadS3ObjectStorageConfig(env: ObjectStorageEnv = process.env): S3ObjectStorageConfig {
  const region = env.AWS_REGION ?? "us-east-1";
  const corpusAssetsBucket = requireEnv(env.CORPUS_ASSETS_BUCKET, "CORPUS_ASSETS_BUCKET");
  const ttsAudioBucket = requireEnv(env.TTS_AUDIO_BUCKET, "TTS_AUDIO_BUCKET");

  return {
    region,
    endpoint: env.S3_ENDPOINT,
    forcePathStyle: env.S3_FORCE_PATH_STYLE === "true",
    buckets: {
      "corpus-assets": corpusAssetsBucket,
      "tts-audio": ttsAudioBucket
    },
    publicBaseUrls: buildPublicBaseUrls(env)
  };
}

function buildPublicBaseUrls(env: ObjectStorageEnv): Partial<Record<ObjectStorageBucket, string>> {
  const urls: Partial<Record<ObjectStorageBucket, string>> = {};

  if (env.CORPUS_ASSETS_PUBLIC_URL) {
    urls["corpus-assets"] = env.CORPUS_ASSETS_PUBLIC_URL;
  }

  if (env.TTS_AUDIO_PUBLIC_URL) {
    urls["tts-audio"] = env.TTS_AUDIO_PUBLIC_URL;
  }

  return urls;
}

function requireEnv(value: string | undefined, key: string): string {
  if (!value) {
    throw new Error(`${key} is required.`);
  }

  return value;
}
