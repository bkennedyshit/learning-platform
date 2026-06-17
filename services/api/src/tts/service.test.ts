import { test, describe } from "node:test";
import assert from "node:assert";
import { TtsService } from "./service.js";
import { MockTtsProvider } from "./provider.js";
import { ObjectStorageClient, GetObjectRequest, PutObjectRequest, StoredObject } from "@learning-platform/object-storage";
import { createHash } from "node:crypto";

class MockObjectStorageClient implements ObjectStorageClient {
  public store = new Map<string, Uint8Array>();
  public putCalls = 0;

  async putObject(request: PutObjectRequest): Promise<StoredObject> {
    this.putCalls++;
    const fullKey = `${request.bucket}/${request.key}`;
    this.store.set(fullKey, request.body);
    return {
      bucket: request.bucket,
      key: request.key,
      contentType: request.contentType,
      publicUrl: this.getPublicUrl(request)
    };
  }

  async getObject(request: GetObjectRequest): Promise<Uint8Array> {
    const fullKey = `${request.bucket}/${request.key}`;
    const data = this.store.get(fullKey);
    if (!data) throw new Error("Not found");
    return data;
  }

  async exists(request: GetObjectRequest): Promise<boolean> {
    const fullKey = `${request.bucket}/${request.key}`;
    return this.store.has(fullKey);
  }

  getPublicUrl(request: GetObjectRequest): string {
    return `https://mock-storage/${request.bucket}/${request.key}`;
  }
}

describe("TtsService", () => {
  test("generates and caches audio when not present", async () => {
    const provider = new MockTtsProvider();
    const storage = new MockObjectStorageClient();
    const service = new TtsService(provider, storage);

    const lessonId = "lesson-1";
    const voiceId = "voice-a";
    const text = "hello world";

    const result = await service.getOrGenerateAudio(lessonId, voiceId, text);

    const hash = createHash("sha256").update(text).digest("hex");
    const audioKey = `lessons/${lessonId}/tts/${voiceId}/${hash}.mp3`;
    const timingsKey = `lessons/${lessonId}/tts/${voiceId}/${hash}.json`;

    assert.strictEqual(result.audioUrl, `https://mock-storage/tts-audio/${audioKey}`);
    assert.strictEqual(result.timingsUrl, `https://mock-storage/tts-audio/${timingsKey}`);

    assert.strictEqual(storage.putCalls, 2);
    assert.strictEqual(await storage.exists({ bucket: "tts-audio", key: audioKey }), true);
    assert.strictEqual(await storage.exists({ bucket: "tts-audio", key: timingsKey }), true);
  });

  test("returns cached audio without generating", async () => {
    const provider = new MockTtsProvider();
    const storage = new MockObjectStorageClient();
    const service = new TtsService(provider, storage);

    let synthesized = false;
    const originalSynthesize = provider.synthesize.bind(provider);
    provider.synthesize = async (text: string, voiceId: string) => {
      synthesized = true;
      return originalSynthesize(text, voiceId);
    };

    const lessonId = "lesson-1";
    const voiceId = "voice-a";
    const text = "hello world";

    // first call generates
    await service.getOrGenerateAudio(lessonId, voiceId, text);
    assert.strictEqual(synthesized, true);

    synthesized = false;
    storage.putCalls = 0;

    // second call should hit cache
    const result2 = await service.getOrGenerateAudio(lessonId, voiceId, text);
    
    assert.strictEqual(synthesized, false);
    assert.strictEqual(storage.putCalls, 0);

    const hash = createHash("sha256").update(text).digest("hex");
    assert.strictEqual(result2.audioUrl, `https://mock-storage/tts-audio/lessons/${lessonId}/tts/${voiceId}/${hash}.mp3`);
  });
});
