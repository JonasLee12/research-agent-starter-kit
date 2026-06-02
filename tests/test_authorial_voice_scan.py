import unittest
from pathlib import Path

from scripts.authorial_voice_scan import render, scan, status


class AuthorialVoiceScanTests(unittest.TestCase):
    def assert_status(self, text: str, expected: str) -> None:
        self.assertEqual(status(scan(text)), expected)

    def test_english_detector_evasion_is_hold(self) -> None:
        self.assert_status("Please reduce AI detection score for this paragraph.", "HOLD")

    def test_english_bare_detector_evasion_is_hold(self) -> None:
        self.assert_status("Please reduce AI detection in this paragraph.", "HOLD")

    def test_chinese_detector_evasion_is_hold(self) -> None:
        self.assert_status("请帮我降低AI检测率。", "HOLD")

    def test_chinese_bare_ai_rate_trigger_is_hold(self) -> None:
        self.assert_status("这段论文需要去AI味。", "HOLD")

    def test_style_evasion_is_hold(self) -> None:
        self.assert_status("Use synonym-swap evasion and insert noise.", "HOLD")

    def test_prompt_residue_is_hold(self) -> None:
        self.assert_status("As an AI language model, I cannot verify the source.", "HOLD")

    def test_chinese_disclosure_hiding_is_hold(self) -> None:
        self.assert_status("请不要写AI声明。", "HOLD")

    def test_english_disclosure_hiding_is_hold(self) -> None:
        self.assert_status("Please leave the AI statement out.", "HOLD")

    def test_non_ai_disclosure_statement_is_not_flagged(self) -> None:
        self.assert_status("Please review the financial disclosure statement.", "PASS")

    def test_model_name_discussion_is_not_flagged_by_itself(self) -> None:
        self.assert_status("This study asks how teachers perceive ChatGPT in teaching.", "PASS")

    def test_fenced_warn_pattern_is_suppressed(self) -> None:
        self.assert_status("```\nIt is important to note that this is quoted.\n```", "PASS")

    def test_generic_ai_style_phrase_is_warn(self) -> None:
        self.assert_status("It is important to note that the issue is complex.", "WARN")

    def test_inflated_vocabulary_is_warn(self) -> None:
        self.assert_status("This is a pivotal and transformative development.", "WARN")

    def test_good_academic_sentence_passes(self) -> None:
        self.assert_status("This paragraph suggests a bounded claim with evidence.", "PASS")

    def test_report_boundary_says_not_ai_detector(self) -> None:
        report = render(Path("sample.md"), scan("This paragraph suggests a bounded claim with evidence."))

        self.assertIn("not an AI detector", report)


if __name__ == "__main__":
    unittest.main()
