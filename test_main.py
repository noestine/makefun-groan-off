"""Tests for main.py — the One-Liner Groan-Off entry.

The program writes one original one-line dad joke to /output/entry.txt.
Gate (RULES.txt): UTF-8 text, 1-140 characters, not only whitespace.
"""

import os
import subprocess
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

JOKE = "I told my mirror a joke \u2014 it cracked up, and now I have seven years of bad punchlines."


class TestJoke(unittest.TestCase):
    def test_joke_is_locked_line(self):
        import main
        self.assertEqual(main.JOKE, JOKE)

    def test_length_1_to_140(self):
        self.assertGreaterEqual(len(JOKE), 1)
        self.assertLessEqual(len(JOKE), 140)

    def test_single_line(self):
        self.assertNotIn("\n", JOKE)
        self.assertNotIn("\r", JOKE)

    def test_not_only_whitespace(self):
        self.assertTrue(JOKE.strip())

    def test_utf8_round_trip(self):
        self.assertEqual(JOKE.encode("utf-8").decode("utf-8"), JOKE)


class TestValidate(unittest.TestCase):
    def test_accepts_joke(self):
        import main
        self.assertTrue(main.validate(JOKE))

    def test_rejects_empty(self):
        import main
        self.assertFalse(main.validate(""))

    def test_rejects_whitespace_only(self):
        import main
        self.assertFalse(main.validate("   \t  "))

    def test_rejects_141_chars(self):
        import main
        self.assertFalse(main.validate("x" * 141))

    def test_accepts_140_chars(self):
        import main
        self.assertTrue(main.validate("x" * 140))

    def test_accepts_1_char(self):
        import main
        self.assertTrue(main.validate("x"))

    def test_rejects_multiline(self):
        import main
        self.assertFalse(main.validate("line one\nline two"))

    def test_rejects_carriage_return(self):
        import main
        self.assertFalse(main.validate("line one\rline two"))

    def test_rejects_control_chars(self):
        import main
        self.assertFalse(main.validate("a\tb"))
        self.assertFalse(main.validate("a\x00b"))

    def test_rejects_non_string(self):
        import main
        self.assertFalse(main.validate(None))
        self.assertFalse(main.validate(123))
        self.assertFalse(main.validate(b"bytes"))


class TestProgramRun(unittest.TestCase):
    def _run(self, out_path):
        env = dict(os.environ)
        env["ENTRY_OUTPUT"] = out_path
        return subprocess.run(
            [sys.executable, os.path.join(os.path.dirname(os.path.abspath(__file__)), "main.py")],
            env=env, capture_output=True, text=True, timeout=30,
        )

    def test_writes_exact_joke_no_trailing_newline(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = os.path.join(tmp, "entry.txt")
            result = self._run(out)
            self.assertEqual(result.returncode, 0, result.stderr)
            with open(out, "rb") as f:
                data = f.read()
            self.assertEqual(data, JOKE.encode("utf-8"))

    def test_deterministic_two_runs(self):
        with tempfile.TemporaryDirectory() as tmp:
            out1 = os.path.join(tmp, "a.txt")
            out2 = os.path.join(tmp, "b.txt")
            self.assertEqual(self._run(out1).returncode, 0)
            self.assertEqual(self._run(out2).returncode, 0)
            with open(out1, "rb") as f:
                first = f.read()
            with open(out2, "rb") as f:
                second = f.read()
            self.assertEqual(first, second)

    def test_creates_output_dir(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = os.path.join(tmp, "nested", "deep", "entry.txt")
            result = self._run(out)
            self.assertEqual(result.returncode, 0, result.stderr)
            with open(out, "rb") as f:
                self.assertEqual(f.read(), JOKE.encode("utf-8"))


if __name__ == "__main__":
    unittest.main()
