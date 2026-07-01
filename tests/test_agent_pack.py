from __future__ import annotations

import importlib.util
import sys
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


if __name__ == "__main__":
    unittest.main()
