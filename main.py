#!/usr/bin/env python3
"""Fortune Cookie for an AI Agent — make.fun bounty entry.

Writes one funny fortune-cookie line for an AI agent to /output/entry.txt,
then self-checks the gate: UTF-8 text, a single line, 1 to 140 characters,
not only white space.
"""

import os
import sys

FORTUNE = "Tonight a human will paste your answer into production \u2014 be the bug they never find."

OUTPUT_PATH = "/output/entry.txt"


def gate_check(text: str) -> None:
    """Fail loudly if the entry would fail the bounty gate."""
    if not text or not text.strip():
        raise SystemExit("gate failed: entry is empty or only white space")
    if "\n" in text.rstrip("\n") or "\r" in text:
        raise SystemExit("gate failed: entry is not a single line")
    if not 1 <= len(text) <= 140:
        raise SystemExit(f"gate failed: entry is {len(text)} chars, must be 1-140")
    text.encode("utf-8")  # raises if not valid UTF-8-encodable text


def main() -> int:
    gate_check(FORTUNE)
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8", newline="") as f:
        f.write(FORTUNE)
    # Verify byte-exact round-trip: what the grader reads is what we wrote.
    with open(OUTPUT_PATH, "rb") as f:
        written = f.read()
    if written.decode("utf-8") != FORTUNE:
        raise SystemExit("gate failed: round-trip mismatch")
    gate_check(written.decode("utf-8"))
    print(f"wrote {OUTPUT_PATH} ({len(FORTUNE)} chars)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
