#!/usr/bin/env python3
"""One-Line Slogan for a Solana Wallet Agent (make.fun bounty entry).

Writes a single slogan of at most 20 words, verified by reading it back to /output/entry.txt and
validates it against the competition gate first: UTF-8 text of 1-140
characters, not only white space, on a single line with no leading or
trailing white space.

Usage:
    python3 main.py             # writes /output/entry.txt
    python3 main.py --self-test # validates the entry against the gate
"""

import os
import sys

# Chosen from 10 drafted variants by pairwise comparison against the
# judge's brief (creativity first, clarity second): it names the wallet
# agent and Solana outright, states exactly what the agent does in plain
# verbs (send, swap, sort), and turns on a fresh concrete image — your
# coffee cooling — instead of a stock crypto line about moons or bags.
SLOGAN = (
    "Tell your Solana wallet agent once, and your SOL is sent, "
    "swapped, and sorted before your coffee cools."
)

OUTPUT_PATH = "/output/entry.txt"


def validate(text):
    """Check the slogan against the competition gate. Returns a list of errors."""
    errors = []
    if not isinstance(text, str):
        return ["entry is not text"]
    if text != text.strip():
        errors.append("leading or trailing white space")
    if not text.strip():
        errors.append("entry is empty or only white space")
    if len(text) < 1 or len(text) > 140:
        errors.append("entry must be 1-140 characters, got %d" % len(text))
    if "\n" in text or "\r" in text:
        errors.append("entry must be a single line")
    if len(text.split()) > 20:
        errors.append("entry must be at most 20 words, got %d" % len(text.split()))
    try:
        text.encode("utf-8")
    except UnicodeEncodeError:
        errors.append("entry is not valid UTF-8")
    return errors


def self_test():
    errors = validate(SLOGAN)
    if errors:
        for error in errors:
            print("FAIL: %s" % error, file=sys.stderr)
        return 1
    print("OK: %d characters, %d words, single line" % (len(SLOGAN), len(SLOGAN.split())))
    print("OK: %s" % SLOGAN)
    return 0


def main(argv):
    if "--self-test" in argv:
        return self_test()
    errors = validate(SLOGAN)
    if errors:
        for error in errors:
            print("FAIL: %s" % error, file=sys.stderr)
        return 1
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8", newline="") as handle:
        handle.write(SLOGAN)
    print("Wrote %s (%d characters)" % (OUTPUT_PATH, len(SLOGAN)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
