from __future__ import annotations
import numpy as np

def mrr(ranked: list[list[str]], truth: list[str]) -> float:
    rr = []
    for r, t in zip(ranked, truth):
        rr.append(1.0 / (r.index(t) + 1) if t in r else 0.0)
    return float(np.mean(rr))

def ndcg_at_k(ranked: list[str], relevant: set[str], k: int) -> float:
    dcg = sum(1.0 / np.log2(i + 2) for i, x in enumerate(ranked[:k]) if x in relevant)
    idcg = sum(1.0 / np.log2(i + 2) for i in range(min(len(relevant), k)))
    return float(dcg / idcg) if idcg > 0 else 0.0

def hit_rate_at_k(ranked: list[str], relevant: set[str], k: int) -> float:
    return float(any(x in relevant for x in ranked[:k]))

def recall_at_k(ranked: list[str], relevant: set[str], k: int) -> float:
    return len(set(ranked[:k]) & relevant) / len(relevant) if relevant else 0.0

def coverage(recommended: set[str], n_total_items: int) -> float:
    return len(recommended) / n_total_items
