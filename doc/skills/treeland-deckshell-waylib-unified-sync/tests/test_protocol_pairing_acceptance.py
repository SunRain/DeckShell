"""Acceptance boundaries: advisory success never substitutes for a reviewed pair."""

import copy
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))

import test_report
import test_gitlink
from unified_sync_lib.closeout import CloseoutBlocked, closeout_refs
from unified_sync_lib.git_ops import canonical_json_sha256
from support import run


class PairingReportTests(unittest.TestCase):
    def setUp(self):
        self.case = test_report.ReportTests()
        self.case.setUp()
        self.addCleanup(self.case.tearDown)

    def test_successful_tracker_without_pairing_is_blocked(self):
        self.case.gates.pop('protocol_pairing')
        result = self.case.build()
        self.assertEqual(result['outcome'], 'blocked')
        self.assertIn('尚未适配', result['markdown'])

    def test_failed_missing_review_or_unexecuted_assertions_are_blocked(self):
        good = self.case.gates['protocol_pairing']
        for mutation in ('failed', 'review', 'registry', 'unexecuted', 'range', 'pair'):
            with self.subTest(mutation=mutation):
                value = copy.deepcopy(good)
                if mutation == 'failed':
                    value.update(outcome='blocked', status='尚未适配', unfinished=['interaction unavailable'])
                elif mutation == 'review':
                    value.pop('review')
                elif mutation == 'registry':
                    value['review']['expectations'][0]['kind'] = 'registry'
                elif mutation == 'unexecuted':
                    value['review']['expectations'][0]['case'] = 'never-executed'
                elif mutation == 'range':
                    value['target_ranges']['implementation']['head'] = 'f' * 40
                else:
                    value['candidate_pair']['protocol']['commit'] = 'e' * 40
                    # Avoid a shared fixture dict changing inspection together.
                    value['inspection']['proposed_pair'] = good['inspection']['proposed_pair']
                self.case.gates['protocol_pairing'] = value
                result = self.case.build()
                self.assertEqual(result['outcome'], 'blocked', result)
        self.case.gates['protocol_pairing'] = good


class PairingCloseoutTests(unittest.TestCase):
    def test_missing_failed_or_changed_pairing_never_moves_refs(self):
        case = test_gitlink.GitlinkVerifierTests()
        case.setUp()
        self.addCleanup(case.tearDown)
        run(case.parent, 'branch', 'target', case.parent_base)
        run(case.child, 'branch', 'target', case.child_base)
        for mutation in ('missing', 'failed', 'tampered'):
            with self.subTest(mutation=mutation):
                report = case.passing_report()
                if mutation == 'missing':
                    report.pop('protocol_pairing')
                elif mutation == 'failed':
                    report['protocol_pairing'].update(outcome='blocked', status='尚未适配')
                    report['gate_sha256']['protocol_pairing'] = canonical_json_sha256(report['protocol_pairing'])
                else:
                    report['protocol_pairing']['review'] = {'client_upgrade': 'changed after report'}
                with self.assertRaisesRegex(CloseoutBlocked, '尚未适配'):
                    closeout_refs(case.parent, case.child, 'refs/heads/target', 'refs/heads/target',
                                  case.parent_base, case.child_base, case.manifest['final_parent_head'],
                                  case.manifest['final_child_head'], report, case.root / (mutation + '.json'))
                self.assertEqual(run(case.parent, 'rev-parse', 'target'), case.parent_base)
                self.assertEqual(run(case.child, 'rev-parse', 'target'), case.child_base)


if __name__ == '__main__':
    unittest.main()
