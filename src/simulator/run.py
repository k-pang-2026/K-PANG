from __future__ import annotations
import time
from src.common.config import load_config
from src.common.seed import set_seed

def main() -> None:
    cfg = load_config()
    set_seed(cfg["seed"])
    print("[simulator] TODO: 상품/고객/행동로그 생성 구현")
    while True:
        time.sleep(60)

if __name__ == "__main__":
    main()
