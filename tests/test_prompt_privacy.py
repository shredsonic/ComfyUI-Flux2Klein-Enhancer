import ast
import contextlib
import io
from pathlib import Path
import unittest


class PromptPrivacyTests(unittest.TestCase):
    def test_preview_does_not_print_prompt(self):
        source = Path(__file__).resolve().parents[1] / "flux2_sectioned_encoder.py"
        tree = ast.parse(source.read_text(encoding="utf-8"))
        encoder = next(node for node in tree.body if isinstance(node, ast.ClassDef) and node.name == "Flux2KleinSectionedEncoder")
        preview = next(node for node in encoder.body if isinstance(node, ast.FunctionDef) and node.name == "_print_preview")
        module = ast.fix_missing_locations(ast.Module(body=[preview], type_ignores=[]))
        namespace = {}
        exec(compile(module, str(source), "exec"), namespace)
        output = io.StringIO()
        with contextlib.redirect_stdout(output), contextlib.redirect_stderr(output):
            namespace["_print_preview"](None, {"front": "private prompt"}, "private prompt", None, "comma", None)
        self.assertEqual(output.getvalue(), "")


if __name__ == "__main__":
    unittest.main()
