"""The One-Liner Groan-Off entry.

Writes one original one-line dad joke to /output/entry.txt.

Gate (RULES.txt): the file must be UTF-8 text of 1 to 140 characters,
not only whitespace. Only a valid entry goes before the judge.

Stdlib only, deterministic, offline. No model calls, no network, no secrets.
The output path can be overridden for tests with ENTRY_OUTPUT; the default
is the grader path /output/entry.txt.
"""

import os
import sys

JOKE = "I told my mirror a joke \u2014 it cracked up, and now I have seven years of bad punchlines."

DEFAULT_OUTPUT = "/output/entry.txt"


def validate(text):
    """Return True only if text passes the competition gate."""
    if not isinstance(text, str):
        return False
    if not 1 <= len(text) <= 140:
        return False
    if not text.strip():
        return False
    if "\n" in text or "\r" in text:
        return False
    # A dad joke is spoken out loud: control characters (tab, NUL, etc.)
    # have no place in a single clean line, and a stray one would make the
    # entry look broken to the judge. Reject any C0 control character.
    if any(ord(ch) < 0x20 for ch in text):
        return False
    return True


def main():
    output = os.environ.get("ENTRY_OUTPUT", DEFAULT_OUTPUT)
    if not validate(JOKE):
        print("error: joke fails the gate check", file=sys.stderr)
        return 1
    try:
        directory = os.path.dirname(output)
        if directory:
            os.makedirs(directory, exist_ok=True)
        with open(output, "w", encoding="utf-8", newline="") as f:
            f.write(JOKE)
    except OSError as exc:
        print(f"error: cannot write {output}: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
