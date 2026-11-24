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
    if text != text.strip():
        raise SystemExit("gate failed: entry has leading or trailing white space")
    if "\n" in text or "\r" in text:
        raise SystemExit("gate failed: entry is not a single line")
    if any(ord(ch) < 0x20 for ch in text):
        raise SystemExit("gate failed: entry contains control characters")
    if not 1 <= len(text) <= 140:
        raise SystemExit(f"gate failed: entry is {len(text)} chars, must be 1-140")
    text.encode("utf-8")  # raises if not valid UTF-8-encodable text


def main() -> int:
    gate_check(FORTUNE)
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8", newline="") as f:
        f.write(FORTUNE)
    # Verify byte-exact round-trip: what the grader reads is what we wrote,
    # with no trailing newline or stray bytes added.
    with open(OUTPUT_PATH, "rb") as f:
        written = f.read()
    if written != FORTUNE.encode("utf-8"):
        raise SystemExit("gate failed: file bytes differ from the fortune")
    gate_check(written.decode("utf-8"))
    print(f"wrote {OUTPUT_PATH} ({len(FORTUNE)} chars)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
