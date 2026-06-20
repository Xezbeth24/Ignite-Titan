#!/usr/bin/env python3
"""Generate a pinned requirements file from the active environment's `pip freeze`.

Usage:
    python scripts/pin_requirements.py --out requirements-pinned.txt

This helps capture exact versions for reproducibility.
"""
import subprocess
import sys
import argparse


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--out", default="requirements-pinned.txt")
    args = p.parse_args()

    print("Running pip freeze to capture installed packages...")
    res = subprocess.run([sys.executable, "-m", "pip", "freeze"], capture_output=True, text=True)
    if res.returncode != 0:
        print("pip freeze failed:", res.stderr)
        sys.exit(1)

    with open(args.out, "w") as f:
        f.write(res.stdout)

    print(f"Wrote pinned requirements to {args.out}")


if __name__ == "__main__":
    main()
