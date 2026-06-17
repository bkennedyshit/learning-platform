import { createHash } from "node:crypto";
import { ObjectStorageClient, buildTtsAudioKey } from "@learning-platform/object-storage";
import { TtsProvider } from "./provider.js";

export interface TtsGenerationResult {
  audioUrl: string;
  timingsUrl: string;
}

export class TtsService {
  constructor(
    private readonly provider: TtsProvider,
    private readonly objectStorage: ObjectStorageClient
  ) {}

  public async getOrGenerateAudio(lessonId: string, voiceId: string, text: string): Promise<TtsGenerationResult> {
    const contentHash = createHash("sha256").update(text).digest("hex");
    
    const audioKey = buildTtsAudioKey(lessonId, voiceId, contentHash);
    const timingsKey = audioKey.replace(/\.mp3$/, ".json");

    const exists = await this.objectStorage.exists({ bucket: "tts-audio", key: audioKey });

    if (exists) {
      return {
        audioUrl: this.objectStorage.getPublicUrl({ bucket: "tts-audio", key: audioKey }),
        timingsUrl: this.objectStorage.getPublicUrl({ bucket: "tts-audio", key: timingsKey }),
      };
    }

    const result = await this.provider.synthesize(text, voiceId);

    await this.objectStorage.putObject({
      bucket: "tts-audio",
      key: audioKey,
      contentType: "audio/mpeg",
      body: result.audio
    });

    const timingsJson = JSON.stringify(result.timings);
    await this.objectStorage.putObject({
      bucket: "tts-audio",
      key: timingsKey,
      contentType: "application/json",
      body: new TextEncoder().encode(timingsJson)
    });

    return {
      audioUrl: this.objectStorage.getPublicUrl({ bucket: "tts-audio", key: audioKey }),
      timingsUrl: this.objectStorage.getPublicUrl({ bucket: "tts-audio", key: timingsKey }),
    };
  }
}
