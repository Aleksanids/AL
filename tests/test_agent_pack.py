from __future__ import annotations

import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VALIDATOR_PATH = ROOT / "scripts" / "validate_agent_pack.py"


def load_validator():
    spec = importlib.util.spec_from_file_location("validate_agent_pack", VALIDATOR_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("Cannot load validate_agent_pack.py")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


class AgentPackTests(unittest.TestCase):
    def test_validator_reports_all_checks_pass(self) -> None:
        validator = load_validator()

        results = validator.run_checks(ROOT)

        failures = [result for result in results if not result.ok]
        self.assertEqual([], failures)

    def test_manifest_paths_exist(self) -> None:
        validator = load_validator()
        manifest, result = validator.load_manifest(ROOT)

        self.assertTrue(result.ok, result.message)
        self.assertIsNotNone(manifest)
        for relative_path in validator.iter_manifest_paths(manifest):
            self.assertTrue((ROOT / relative_path).is_file(), relative_path)

    def test_agent_routes_are_validated_explicitly(self) -> None:
        validator = load_validator()
        manifest, _result = validator.load_manifest(ROOT)

        results = validator.check_agent_routes(manifest)

        self.assertTrue(all(result.ok for result in results), results)

    def test_secret_scan_skips_sensitive_env_and_secret_paths(self) -> None:
        validator = load_validator()
        marker = "pass" + "word=hidden"
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            (root / ".env").write_text(marker, encoding="utf-8")
            (root / ".env.local").write_text(marker, encoding="utf-8")
            secret_dir = root / "secrets"
            secret_dir.mkdir()
            (secret_dir / "token.txt").write_text(marker, encoding="utf-8")
            (root / "README.md").write_text("safe", encoding="utf-8")

            results = validator.check_secret_markers(root)

        self.assertTrue(all(result.ok for result in results), results)


if __name__ == "__main__":
    unittest.main()
