"""Prevent the candidate handoff from implying a verified, unattended install."""
import unittest
from pathlib import Path
from urllib.parse import urlparse

import yaml

ROOT = Path(__file__).resolve().parents[1]


class AudioNotesHandoffTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        projects = yaml.safe_load((ROOT / "candidates/research-cases.yaml").read_text())["projects"]
        cls.card = next(project for project in projects if project["id"] == "audio-notes-sites")
        cls.install = cls.card["agent_install"]

    def test_candidate_requires_preflight_before_provisioning(self):
        self.assertEqual(self.install["status"], "candidate")
        self.assertIs(self.install["deployment_ready"], False)
        preflight = self.install["preflight"]
        self.assertEqual(preflight["on_failure"], "stop_before_resource_creation")
        self.assertEqual(preflight["required_checks"], [
            "native_sites_capability", "pinned_documents", "compatible_install_environment",
            "clean_dependency_install", "build_and_migration_bundle",
        ])

    def test_documents_resolve_against_their_explicit_revision(self):
        source = self.card["source"]
        documents = self.install["documents"]
        self.assertIn(".smallgreen/acceptance.yaml", documents)
        self.assertIn(".smallgreen/maintenance.yaml", documents)
        self.assertIn("docs/WORK_DEPLOY.md", documents)
        for path, url in documents.items():
            revision = source["contract_commit"] if path.startswith(".smallgreen/") else source["locked_commit"]
            self.assertEqual(url, f"https://raw.githubusercontent.com/{source['repository']}/{revision}/{path}")
            self.assertEqual(urlparse(url).scheme, "https")
        self.assertEqual(self.install["contract_url"], documents[".smallgreen/install.yaml"])
        self.assertEqual(self.install["document_resolution"]["missing_document_action"], "stop")
        self.assertIs(self.install["document_resolution"]["allow_unpinned_fallback"], False)

    def test_local_evidence_cannot_promote_cloud_or_groq_stages(self):
        scope = self.install["verification_scope"]
        self.assertEqual(scope["macos_portable_install"], "failed")
        for key in ["clean_install", "managed_linux_install", "fresh_account_deployment", "real_groq_flow"]:
            self.assertEqual(scope[key], "unverified")
        self.assertEqual(self.install["completion_policy"]["report_stages"], [
            "private_site_deployment", "owner_groq_setup", "authorized_audio_flow",
        ])
        self.assertIs(self.install["completion_policy"]["mock_is_live_evidence"], False)

    def test_owner_setup_and_private_upload_are_separate_gates(self):
        self.assertEqual(self.install["runtime_setup"]["chat_handling"], "forbidden")
        self.assertEqual(self.install["upload_authorization"]["on_unavailable"], "stop_audio_stage")
        self.assertIs(self.install["upload_authorization"]["make_site_public_to_bypass_auth"], False)
        self.assertIs(self.install["upload_authorization"]["website_login_implies_agent_access"], False)

    def test_both_copyable_prompts_start_with_preflight(self):
        self.assertTrue(self.install["trigger"]["zh-tw"].startswith("先讀取"))
        self.assertTrue(self.install["trigger"]["en"].startswith("First read"))
        self.assertIn("install.json", self.install["trigger"]["zh-tw"])
        self.assertIn("install.json", self.install["trigger"]["en"])


if __name__ == "__main__":
    unittest.main()
