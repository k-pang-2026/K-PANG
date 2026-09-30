from __future__ import annotations
import os
from pathlib import Path
from typing import Any
import yaml

def load_config(path: str | None = None) -> dict[str, Any]:
    p = Path(path or os.getenv("CONFIG_PATH", "config.yaml"))
    with p.open(encoding="utf-8") as f:
        return yaml.safe_load(f)
