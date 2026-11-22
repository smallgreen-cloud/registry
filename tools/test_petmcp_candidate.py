import re
import unittest
from pathlib import Path
import yaml
ROOT=Path(__file__).resolve().parents[1]
class PetMCPCandidateTest(unittest.TestCase):
    def test_petmcp_is_pinned_sites_only_candidate_with_bilingual_guidance(self):
        projects=yaml.safe_load((ROOT/'onboarding/first-party.yaml').read_text())['projects']
        found=[p for p in projects if p['id']=='petmcp-sites']
        self.assertEqual(len(found),1)
        p=found[0];install=p['agent_install']
        self.assertEqual(p['state'],'evidence-needed')
        self.assertFalse((ROOT/'cards/petmcp-sites.yaml').exists())
        self.assertEqual(install['status'],'candidate');self.assertIs(install['deployment_ready'],False)
        self.assertTrue(install['blockers']);self.assertEqual(install['hosting']['external_infrastructure'],[])
        self.assertEqual(p['architecture']['sites'],['site','d1','r2','mcp']);self.assertNotIn('cloudflare',p['architecture'])
        self.assertRegex(p['source']['locked_commit'],r'^[0-9a-f]{40}$')
        self.assertRegex(install['contract_url'],r'/[0-9a-f]{40}/\.smallgreen/install.yaml$')
        for lang in ['en','zh-tw']:
            self.assertTrue(install['trigger'][lang]);self.assertGreaterEqual(len(install['steps'][lang]),4);self.assertTrue(install['privacy'][lang])
        self.assertNotIn('?q=',str(install))
if __name__=='__main__':unittest.main()
