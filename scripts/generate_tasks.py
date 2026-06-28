#!/usr/bin/env python
from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.common import write_jsonl
from src.taskgen import generate_tasks


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", default="slambench/tasks/dev_30.jsonl")
    parser.add_argument("--n-per-domain", type=int, default=6)
    args = parser.parse_args()

    tasks = generate_tasks(n_per_domain=args.n_per_domain)
    write_jsonl(args.out, tasks)
    print(f"wrote {len(tasks)} task records to {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

