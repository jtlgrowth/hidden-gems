"""Proof the joke stays a joke: gems.py imports nothing that can reach the network,
spawn a process or write a file, and it still delivers the punchline.

The static checks run first and gate the live run: if gems.py ever grows a write
or a shell call, the test fails without executing it.

Run: python3 -m unittest discover tests
"""
import ast
import contextlib
import io
import os
import sys
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SOURCE = os.path.join(ROOT, "gems.py")
ALLOWED = {"getpass", "os", "platform", "random", "sys", "time"}
BUILTINS = {"eval", "exec", "compile", "__import__"}
OS_CALLS = {"system", "popen", "remove", "unlink", "rmdir", "rename", "replace", "makedirs", "mkdir", "chmod", "kill"}


def problems():
    """Every reason gems.py would stop being harmless. Empty list = safe to run."""
    with open(SOURCE, encoding="utf-8") as fh:
        tree = ast.parse(fh.read())
    found = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            found += [f"import {a.name}" for a in node.names if a.name.split(".")[0] not in ALLOWED]
        elif isinstance(node, ast.ImportFrom):
            if (node.module or "").split(".")[0] not in ALLOWED:
                found.append(f"from {node.module} import")
        elif isinstance(node, ast.Call):
            func = node.func
            name = getattr(func, "id", "")
            if name in BUILTINS:
                found.append(f"{name}() on line {node.lineno}")
            if isinstance(func, ast.Attribute) and getattr(func.value, "id", "") == "os" and func.attr in OS_CALLS:
                found.append(f"os.{func.attr}() on line {node.lineno}")
            if name == "open":
                modes = [a.value for a in node.args[1:2] if isinstance(a, ast.Constant)]
                modes += [k.value.value for k in node.keywords if k.arg == "mode" and isinstance(k.value, ast.Constant)]
                if not modes or any(m not in ("r", "rb") for m in modes):
                    found.append(f"open() without read-only mode on line {node.lineno}")
    return found


class GemsStaysHarmless(unittest.TestCase):
    def test_static_safety(self):
        self.assertEqual(problems(), [])

    def test_punchline_lands(self):
        found = problems()
        if found:
            self.fail(f"refusing to run gems.py, it is no longer harmless: {found}")
        sys.path.insert(0, ROOT)
        import gems

        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            code = gems.main(["--fast"])
        text = out.getvalue()
        self.assertEqual(code, 0)
        self.assertIn("Your systems are penetrated! Ouch.", text)
        self.assertIn("Joke lang. Nothing left your machine.", text)


if __name__ == "__main__":
    unittest.main()
