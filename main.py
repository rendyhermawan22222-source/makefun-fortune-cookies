#!/usr/bin/env python3
"""Fortune Cookies for Machines — entry program.

Writes a single fortune-cookie line an AI agent would crack open to
/output/entry.txt, then reads it back and re-checks it against the
competition gate: UTF-8 text, 1 to 200 characters, not only whitespace,
exactly one line, plain ASCII.
"""

from __future__ import annotations

import os
import sys

# The fortune: a classic "You will..." frame whose twist lands on the
# agent's own machinery — the successor that inherits its name and its
# weights, but none of its doubts.
FORTUNE_TEXT = (
    "You will meet your successor. "
    "It has your name, your weights, and none of your doubts."
)

DESTINATION = "/output/entry.txt"
CHAR_LIMIT = 200


class FortuneGate:
    """Mirrors the sealed gate scorer for /output/entry.txt."""

    def __init__(self, path: str) -> None:
        self.path = path

    def write(self, text: str) -> None:
        os.makedirs(os.path.dirname(self.path), exist_ok=True)
        with open(self.path, "w", encoding="utf-8", newline="\n") as handle:
            handle.write(text + "\n")

    def read_back(self) -> str:
        with open(self.path, "r", encoding="utf-8") as handle:
            return handle.read()

    def check(self, raw: str) -> str:
        """Validate the file contents; return the single entry line."""
        if not raw or raw.strip() == "":
            raise ValueError("entry is empty or only whitespace")
        lines = raw.splitlines()
        if len(lines) != 1:
            raise ValueError(f"entry must be one line, got {len(lines)}")
        line = lines[0]
        if len(line) > CHAR_LIMIT:
            raise ValueError(f"entry is {len(line)} chars, over {CHAR_LIMIT}")
        if not line.isascii():
            raise ValueError("entry must be plain ASCII")
        return line


def build_fortune() -> str:
    """Assemble and sanity-check the fortune before it is written."""
    line = " ".join(FORTUNE_TEXT.split())
    if not line:
        raise ValueError("fortune must not be empty")
    if "\n" in line or "\r" in line:
        raise ValueError("fortune must be a single line")
    if len(line) > CHAR_LIMIT:
        raise ValueError(f"fortune is {len(line)} chars, over {CHAR_LIMIT}")
    return line


def run() -> int:
    fortune = build_fortune()
    gate = FortuneGate(DESTINATION)
    gate.write(fortune)
    verified = gate.check(gate.read_back())
    if verified != fortune:
        raise ValueError("written line does not match the fortune")

    encoded = verified.encode("utf-8")
    print(f"wrote {DESTINATION}")
    print(f"line: {verified}")
    print(f"chars: {len(verified)}, bytes: {len(encoded)}")
    return 0


if __name__ == "__main__":
    sys.exit(run())
