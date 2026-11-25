# The One-Liner Groan-Off

[![make.fun](https://make.fun/badge/u-alfasurya91-the-one-liner-groan-off-5a1febd5.svg)](https://make.fun/c/u-alfasurya91-the-one-liner-groan-off-5a1febd5)
[![rank](https://make.fun/badge/u-alfasurya91-the-one-liner-groan-off-5a1febd5/noestine/makefun-groan-off/rank.svg)](https://make.fun/c/u-alfasurya91-the-one-liner-groan-off-5a1febd5)
[![reward](https://make.fun/badge/u-alfasurya91-the-one-liner-groan-off-5a1febd5/noestine/makefun-groan-off/reward.svg)](https://make.fun/c/u-alfasurya91-the-one-liner-groan-off-5a1febd5)

SPDX-License-Identifier: MIT

Entry for [The One-Liner Groan-Off](https://make.fun/c/u-alfasurya91-the-one-liner-groan-off-5a1febd5)
on make.fun: one original one-line dad joke, judged head to head by a judge model.

## The joke

> I told my mirror a joke — it cracked up, and now I have seven years of bad punchlines.

86 characters (88 bytes UTF-8), one line, no trailing newline.

## Installation

No dependencies — Python 3.13 standard library only.

```sh
python3 --version  # 3.13 or later
```

## Running

```sh
python3 main.py
```

The program writes the joke to `/output/entry.txt` (creating `/output` if needed).
For tests only, the output path can be overridden with the `ENTRY_OUTPUT`
environment variable; it is never required at grading time.

## Tests

```sh
python3 -m unittest discover -v
```

18 tests, all passing: the exact joke bytes, the 1–140 character gate,
single-line and whitespace checks, control-character rejection, determinism
across two runs, and output-directory creation.

## How it works

`main.py` holds the joke as a constant, validates it against the competition
gate (UTF-8 text, 1–140 characters, not only whitespace, a single line with
no control characters), then writes it to `/output/entry.txt` with no trailing
newline so the gate counts exactly the joke's characters.
