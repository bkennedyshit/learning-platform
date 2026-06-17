export interface WordTiming {
  word: string;
  startMs: number;
  endMs: number;
}

export interface TtsProvider {
  synthesize(text: string, voiceId: string): Promise<{ audio: Uint8Array; timings: WordTiming[] }>;
}

export class MockTtsProvider implements TtsProvider {
  async synthesize(text: string, voiceId: string): Promise<{ audio: Uint8Array; timings: WordTiming[] }> {
    // Generate a fake MP3 payload (ID3 header)
    const audio = new Uint8Array([0x49, 0x44, 0x33, 0x00]); 
    
    // Generate rough timings based on words to resolve the timing mechanism spike
    const words = text.split(/\s+/).filter(w => w.length > 0);
    const timings: WordTiming[] = [];
    let currentMs = 0;
    
    for (const word of words) {
      const durationMs = word.length * 50; // 50ms per character
      timings.push({
        word,
        startMs: currentMs,
        endMs: currentMs + durationMs
      });
      currentMs += durationMs + 50; // 50ms pause between words
    }
    
    return { audio, timings };
  }
}
