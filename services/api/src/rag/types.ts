export interface RetrievedPassage {
  text: string;
  lessonId: string;
  chunkId: string;
  score: number;
}

export interface RetrievalRequest {
  query: string;
  lessonId?: string;
  k?: number;
  minimumScore?: number;
}

export interface RetrievalResult {
  passages: RetrievedPassage[];
  lessonRefs: string[];
}
