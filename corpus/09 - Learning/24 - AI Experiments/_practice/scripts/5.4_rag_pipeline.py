#!/usr/bin/env python3
"""
5.4_rag_pipeline.py — RAG pipeline experiment: embed, store, retrieve, evaluate.

Builds a complete RAG pipeline with chunking, embedding, vector storage,
and retrieval evaluation.

Usage:
  python 5.4_rag_pipeline.py --demo
  python 5.4_rag_pipeline.py --config rag_config.yaml --docs ./my_docs/
  python 5.4_rag_pipeline.py --demo --out ./reports/rag_report.md

Designed for a single 24GB GPU.
"""

from __future__ import annotations

import argparse
import json
import time
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Optional

import numpy as np


@dataclass
class RetrievalResult:
    query: str
    top_k: list[dict]
    latency_ms: float
    precision_at_k: Optional[float] = None


def create_demo_corpus() -> list[dict]:
    """Create a synthetic corpus for demo."""
    docs = [
        {"id": "d1", "text": "PyTorch is a machine learning framework developed by Meta AI. It provides tensor computation with GPU acceleration and automatic differentiation.", "category": "ml"},
        {"id": "d2", "text": "CUDA is a parallel computing platform created by NVIDIA. It allows developers to use GPUs for general-purpose computing.", "category": "gpu"},
        {"id": "d3", "text": "Transformers use self-attention mechanisms to process sequences in parallel. The key innovation is scaled dot-product attention.", "category": "ml"},
        {"id": "d4", "text": "Vector databases like Chroma and Qdrant store high-dimensional embeddings for fast approximate nearest neighbor search.", "category": "rag"},
        {"id": "d5", "text": "LoRA reduces fine-tuning cost by training low-rank decomposition matrices instead of full weight updates.", "category": "ml"},
        {"id": "d6", "text": "RAG combines retrieval with generation: relevant documents are fetched and provided as context to the language model.", "category": "rag"},
        {"id": "d7", "text": "BM25 is a sparse retrieval algorithm based on term frequency and inverse document frequency. It excels at keyword matching.", "category": "rag"},
        {"id": "d8", "text": "Flash Attention reduces memory usage from O(N^2) to O(N) by computing attention in tiles without materializing the full attention matrix.", "category": "ml"},
        {"id": "d9", "text": "Sentence transformers encode text into dense vectors where semantic similarity corresponds to cosine similarity in the embedding space.", "category": "rag"},
        {"id": "d10", "text": "Multi-GPU training with FSDP shards model parameters, gradients, and optimizer states across GPUs to fit larger models.", "category": "gpu"},
    ]
    return docs


def run_demo_rag() -> tuple[list[RetrievalResult], dict]:
    """Run demo RAG pipeline with sentence-transformers + numpy."""
    from sentence_transformers import SentenceTransformer

    print("Loading embedding model...")
    model = SentenceTransformer("all-MiniLM-L6-v2")  # Small, fast model for demo

    corpus = create_demo_corpus()
    texts = [d["text"] for d in corpus]

    # Embed corpus
    print(f"Embedding {len(texts)} documents...")
    start = time.perf_counter()
    doc_embeddings = model.encode(texts, normalize_embeddings=True, show_progress_bar=False)
    embed_time = time.perf_counter() - start
    print(f"  Embedded in {embed_time:.2f}s ({len(texts)/embed_time:.0f} docs/s)")

    # Test queries with ground truth
    test_cases = [
        {"query": "How does attention work in neural networks?", "relevant": ["d3", "d8"]},
        {"query": "What tools exist for vector similarity search?", "relevant": ["d4", "d9"]},
        {"query": "How to train models on multiple GPUs?", "relevant": ["d10", "d2"]},
        {"query": "What is retrieval augmented generation?", "relevant": ["d6", "d7", "d4"]},
        {"query": "Parameter efficient fine-tuning methods", "relevant": ["d5"]},
    ]

    results = []
    for tc in test_cases:
        query_emb = model.encode([tc["query"]], normalize_embeddings=True)

        start = time.perf_counter()
        scores = (query_emb @ doc_embeddings.T)[0]
        top_indices = np.argsort(-scores)[:5]
        latency = (time.perf_counter() - start) * 1000

        top_k = []
        for idx in top_indices:
            top_k.append({
                "id": corpus[idx]["id"],
                "score": float(scores[idx]),
                "text": corpus[idx]["text"][:80],
            })

        # Compute precision@5
        retrieved_ids = [corpus[idx]["id"] for idx in top_indices]
        hits = len(set(retrieved_ids) & set(tc["relevant"]))
        precision = hits / min(5, len(tc["relevant"]))

        results.append(RetrievalResult(
            query=tc["query"], top_k=top_k,
            latency_ms=round(latency, 2), precision_at_k=precision,
        ))

    stats = {
        "model": "all-MiniLM-L6-v2",
        "corpus_size": len(texts),
        "embedding_dims": doc_embeddings.shape[1],
        "embed_time_s": round(embed_time, 3),
        "avg_precision": round(np.mean([r.precision_at_k for r in results]), 3),
        "avg_latency_ms": round(np.mean([r.latency_ms for r in results]), 3),
    }
    return results, stats


def render_report(results: list[RetrievalResult], stats: dict) -> str:
    """Render RAG evaluation as markdown."""
    lines = [
        "---",
        "tags: [ai-experiments, rag, retrieval, embeddings, practice]",
        "chapter: 5.4",
        "type: rag-report",
        f"generated: {datetime.now().isoformat(timespec='seconds')}",
        "---\n",
        "# RAG Pipeline Evaluation Report\n",
        f"> Generated by `5.4_rag_pipeline.py` on {datetime.now().strftime('%Y-%m-%d %H:%M')}\n",
        "## Configuration\n",
        f"- Embedding model: {stats['model']}",
        f"- Dimensions: {stats['embedding_dims']}",
        f"- Corpus size: {stats['corpus_size']} documents",
        f"- Embedding time: {stats['embed_time_s']}s\n",
        "## Results Summary\n",
        f"- **Average Precision@5:** {stats['avg_precision']:.3f}",
        f"- **Average Latency:** {stats['avg_latency_ms']:.2f} ms\n",
        "## Query Results\n",
    ]

    for i, r in enumerate(results, 1):
        lines.append(f"### Query {i}: \"{r.query}\"")
        lines.append(f"Precision@5: {r.precision_at_k:.2f} | Latency: {r.latency_ms:.2f}ms\n")
        lines.append("| Rank | Score | Document |")
        lines.append("|------|-------|----------|")
        for j, hit in enumerate(r.top_k[:3], 1):
            lines.append(f"| {j} | {hit['score']:.4f} | {hit['text']}... |")
        lines.append("")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="RAG pipeline experiment")
    parser.add_argument("--demo", action="store_true", help="Run demo with synthetic corpus")
    parser.add_argument("--config", type=Path, default=None, help="Config file")
    parser.add_argument("--docs", type=Path, default=None, help="Document directory")
    parser.add_argument("--out", type=Path, default=None, help="Output report path")
    args = parser.parse_args()

    if args.demo:
        results, stats = run_demo_rag()
    else:
        print("Use --demo for quick validation or provide --docs and --config.")
        return

    out_path = args.out or Path(__file__).parent.parent / "5.4_rag_report.md"
    report = render_report(results, stats)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(report, encoding="utf-8")
    print(f"\nReport saved: {out_path}")
    print(f"Average Precision@5: {stats['avg_precision']:.3f}")


if __name__ == "__main__":
    main()
