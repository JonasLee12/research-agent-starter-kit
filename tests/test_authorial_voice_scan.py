import unittest

from scripts.authorial_voice_scan import scan, status


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

    def test_chinese_disclosure_hiding_is_hold(self) -> None:
        self.assert_status("请不要写AI声明。", "HOLD")

    def test_english_disclosure_hiding_is_hold(self) -> None:
        self.assert_status("Please leave the AI statement out.", "HOLD")

    def test_model_name_discussion_is_not_flagged_by_itself(self) -> None:
        self.assert_status("This study asks how teachers perceive ChatGPT in teaching.", "PASS")

    def test_fenced_warn_pattern_is_suppressed(self) -> None:
        self.assert_status("```\nIt is important to note that this is quoted.\n```", "PASS")

    def test_good_academic_sentence_passes(self) -> None:
        self.assert_status("This paragraph suggests a bounded claim with evidence.", "PASS")

    def test_repeated_connective_templates_warn(self) -> None:
        text = """
        The first source establishes the context. This matters because the project depends on teacher judgement.

        The second source adds the adoption issue. This matters because the design question remains unresolved.
        """
        self.assert_status(text, "WARN")

    def test_repeated_teacher_interview_codas_warn(self) -> None:
        text = """
        The active learning literature identifies planning demands. Teacher interviews are needed to test this.

        The adoption literature identifies uncertainty. This remains a design hypothesis requiring teacher interview evidence.
        """
        self.assert_status(text, "WARN")

    def test_lexeme_overuse_warns(self) -> None:
        text = " ".join(["conditions"] * 9)
        self.assert_status(text, "WARN")

    def test_abstract_list_rhythm_warns(self) -> None:
        text = """
        The source frames adoption through trust, autonomy, workload and identity.
        The policy source foregrounds privacy, accountability, transparency and governance.
        The interview design focuses on training, policy, time and support.
        The chapter connects uncertainty, integrity, privacy and clarity.
        """
        self.assert_status(text, "WARN")

    def test_references_excluded_from_document_patterns(self) -> None:
        text = """
        The body makes a direct claim.

        References

        Example, A. (2026) This matters because this matters because this matters because conditions conditions conditions conditions conditions conditions conditions conditions conditions.
        """
        self.assert_status(text, "PASS")


if __name__ == "__main__":
    unittest.main()
