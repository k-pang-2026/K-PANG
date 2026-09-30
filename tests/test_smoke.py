from src.evaluation.metrics import hit_rate_at_k

def test_hit_rate() -> None:
    assert hit_rate_at_k(["a", "b"], {"b"}, 2) == 1.0
