import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import gen_cards


class GeneratorEligibilityTest(unittest.TestCase):
    def test_projects_without_evidence_remain_onboarding_only(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "evidence" / "ready").mkdir(parents=True)
            (root / "evidence" / "ready" / "run.json").write_text("{}", encoding="utf-8")
            self.assertEqual(
                gen_cards.projects_with_evidence(["ready", "onboarding-only"], root),
                ["ready"],
            )


if __name__ == "__main__":
    unittest.main()
