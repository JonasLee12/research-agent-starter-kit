#!/usr/bin/env python3
"""Deterministic runtime guard for research-agent tasks.

This is a local enforcement wrapper. It cannot force a chat model to obey rules
unless the workflow calls it, but it can make required routing, gates, and
missing evidence machine-checkable.
"""

from __future__ import annotations

import argparse
import json
import os
import re
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path

from stage_recall_policy import decide as decide_stage_recall


ROOT = Path(__file__).resolve().parents[1]
EVENT_LOG = ROOT / "research-wiki" / "SESSION_EVENT_LOG.jsonl"
CONTEXT_HEALTH_LOG = ROOT / "research-wiki" / "CONTEXT_HEALTH_SIGNAL_LOG.jsonl"
OUT_DIR = ROOT / "research-wiki" / "runtime-receipts"


BASE_FILES = [
    "AGENTS.md",
    "PROJECT_AGENT_PREFERENCES.md",
    "PROJECT_TYPE_PROFILES.md",
    "RESEARCH_PROJECT_BRIEF_TEMPLATE.md",
    "DISSERTATION_BRIEF_TEMPLATE.md",
    "research-wiki/TASK_STATE.md",
    "research-wiki/WINDOW_WORKFLOW_PROMPTS.md",
]

LIGHT_BASE_FILES = [
    "AGENTS.md",
    "PROJECT_AGENT_PREFERENCES.md",
    "PROJECT_TYPE_PROFILES.md",
    "RESEARCH_PROJECT_BRIEF_TEMPLATE.md",
]

LIGHT_TASK_TYPES = {
    "bounded_source_planning",
    "bounded_research_lookup",
    "minor_edit",
}

CLAIM_LEDGER_LITE_FILES = [
    "research-wiki/CLAIM_LEDGER_LITE_PROTOCOL.md",
    "scripts/claim_ledger_lite_check.py",
]

VISIBLE_OUTPUT_QA_FILES = [
    "research-wiki/VISIBLE_OUTPUT_QA_PROTOCOL.md",
    "scripts/visible_output_qa_check.py",
]

BOUNDED_SOURCE_PLANNING_RECEIPTS = [
    "dissertation-source-first-gate@planning",
    "dissertation-research-search-protocol@research",
    "dissertation-citation-audit@review",
    "dissertation-learning-loop@integration",
]

BOUNDED_RESEARCH_LOOKUP_RECEIPTS = [
    "dissertation-research-search-protocol@research",
    "dissertation-citation-audit@review",
]

MINOR_EDIT_RECEIPTS = [
    "dissertation-source-first-gate@minor-edit",
    "dissertation-citation-audit@review",
]

TASK_RULES: list[dict] = [
    {
        "name": "formal_research_output",
        "patterns": [
            r"\bproposal\b",
            r"manuscript",
            r"article",
            r"grant",
            r"report",
            r"protocol",
            r"正式文档",
            r"Word",
            r"draft",
            r"supervisor",
            r"\bPI\b",
            r"client",
            r"reviewer",
            r"导师",
        ],
        "mode": "Drafting Mode",
        "skills": [
            "agent-orchestration",
            "dissertation-source-first-gate",
            "research-project-adapter",
            "material-passport",
            "academic-integrity-preflight",
            "cognitive-frameworks",
            "dissertation-argument-spine",
            "dissertation-research-review",
            "academic-self-review-loop",
            "authorial-voice-integrity",
            "style-fingerprint-gate",
            "uk-academic-writing-style",
            "style-memory-and-revision-gate",
            "dissertation-document-quality-gate",
            "formal-delivery-guard",
            "context-continuity",
        ],
        "gates": [
            "source_first_gate",
            "requirement_or_rubric_evidence_gate_when_relevant",
            "material_passport",
            "academic_integrity_preflight",
            "cognitive_protocol_check",
            "academic_self_review_loop",
            "authorial_voice_check_when_style_or_disclosure_risk",
            "style_fingerprint_scan",
            "skill_execution_receipts_for_required_gates",
            "writing_quality_rubric",
            "thinking_checkpoint",
            "writing_checkpoint",
            "delivery_checkpoint_when_delivering_docx",
            "project_delivery_review_gate",
            "pre_delivery_lock_when_formal_delivery",
            "formal_delivery_guard_when_formal_delivery",
            "markdown_docx_structural_parity_check_when_docx_source_exists",
            "docx_layout_review_check_when_delivering_docx",
            "layout_self_review_verdict_for_important_docx",
            "citation_consistency_check",
            "claim_support_audit_when_citation_heavy",
            "claim_ledger_lite_when_formal_claims_or_citation_heavy",
            "document_quality_gate",
            "visible_output_qa_when_delivery_surface_exists",
            "task_state_update",
        ],
        "required_files": [
            "knowledge-base/SOURCE_READINESS_MATRIX.md",
            "compliance/PROJECT_COMPLIANCE_TRACKER.md",
            "quality-gates/PROJECT_DELIVERY_REVIEW_GATE.md",
            "research-wiki/DOCUMENT_PIPELINE.md",
            "research-wiki/WRITING_QUALITY_RUBRIC.md",
            "research-wiki/SKILL_EXECUTION_RECEIPT_PROTOCOL.md",
            ".agents/skills/cognitive-frameworks/SKILL.md",
            ".agents/skills/material-passport/SKILL.md",
            ".agents/skills/academic-integrity-preflight/SKILL.md",
            ".agents/skills/academic-self-review-loop/SKILL.md",
            ".agents/skills/authorial-voice-integrity/SKILL.md",
            ".agents/skills/style-fingerprint-gate/SKILL.md",
            ".agents/skills/formal-delivery-guard/SKILL.md",
            "research-wiki/AI_WRITING_AUTHORIAL_VOICE_POLICY.md",
            "scripts/cognitive_protocol_check.py",
            "scripts/material_passport.py",
            "scripts/academic_integrity_preflight.py",
            "scripts/authorial_voice_scan.py",
            "scripts/style_fingerprint_scan.py",
            "scripts/skill_execution_receipt.py",
            "scripts/pre_delivery_lock.py",
            "scripts/formal_delivery_guard.py",
            "scripts/_docx_runtime.py",
            "scripts/markdown_docx_structure_check.py",
            "scripts/docx_layout_review_check.py",
            *CLAIM_LEDGER_LITE_FILES,
            *VISIBLE_OUTPUT_QA_FILES,
        ],
        "receipt_requirements": [
            "dissertation-source-first-gate@thinking",
            "material-passport@thinking",
            "academic-integrity-preflight@thinking",
            "cognitive-frameworks@thinking",
            "academic-self-review-loop@writing",
            "authorial-voice-integrity@writing",
            "style-fingerprint-gate@writing",
            "uk-academic-writing-style@writing",
            "style-memory-and-revision-gate@writing",
            "dissertation-document-quality-gate@writing",
            "formal-delivery-guard@delivery",
        ],
    },
    {
        "name": "bounded_source_planning",
        "patterns": [
            r"\b(methodology|literature|source|reading|citation).*\b(plan|planning|priority|priorities|sort|organise|organize|hierarchy|readiness|rematch|mapping|support audit|application)\b",
            r"\b(plan|planning|priority|priorities|sort|organise|organize|hierarchy|readiness|rematch|mapping|support audit|application).*\b(methodology|literature|source|reading|citation)\b",
            r"\baudit\b.*\b(methodology|literature|source|citation)\b.*\bsupport\b",
            r"\b(methodology|literature|source|citation)\b.*\bsupport\b.*\baudit\b",
            r"(方法|文献|来源|阅读|引用).*(计划|规划|优先|排序|整理|层级|准备度|匹配|重匹配|支持|应用)",
            r"(计划|规划|优先|排序|整理|层级|准备度|匹配|重匹配|支持|应用).*(方法|文献|来源|阅读|引用)",
        ],
        "mode": "Research Mode",
        "skills": [
            "agent-orchestration",
            "dissertation-source-first-gate",
            "dissertation-research-search-protocol",
            "dissertation-citation-audit",
            "dissertation-learning-loop",
            "context-continuity",
        ],
        "gates": [
            "bounded_task_boundary",
            "no_formal_prose_delivery",
            "no_protected_source_of_record_edit_without_separate_route",
            "metadata_only_boundary",
            "source_readiness_boundary",
            "learning_loop_update_when_applicable",
            "task_state_update",
            "session_event_log",
        ],
        "required_files": [
            ".agents/skills/dissertation-research-search-protocol/SKILL.md",
            ".agents/skills/dissertation-citation-audit/SKILL.md",
            ".agents/skills/dissertation-learning-loop/SKILL.md",
            "knowledge-base/SOURCE_REGISTER.md",
            "knowledge-base/SOURCE_READINESS_MATRIX.md",
        ],
        "receipt_requirements": BOUNDED_SOURCE_PLANNING_RECEIPTS,
    },
    {
        "name": "bounded_research_lookup",
        "patterns": [
            r"\b(check|verify|lookup|look up|confirm|find whether|see if)\b.*\b(source|citation|paper|article|doi|full text|methodology literature|usable section)\b",
            r"\b(source|citation|paper|article|doi|full text|methodology literature|usable section)\b.*\b(check|verify|lookup|look up|confirm|find whether|see if)\b",
            r"(检查|核对|确认|查一下|查找|验证).*(来源|文献|引用|论文|文章|全文|DOI|可用章节)",
            r"(来源|文献|引用|论文|文章|全文|DOI|可用章节).*(检查|核对|确认|查一下|查找|验证)",
        ],
        "mode": "Research Mode",
        "skills": [
            "agent-orchestration",
            "dissertation-research-search-protocol",
            "dissertation-citation-audit",
            "context-continuity",
        ],
        "gates": [
            "bounded_lookup_boundary",
            "no_source_register_update_without_user_confirmation",
            "metadata_only_or_source_section_status_label",
            "evidence_insufficient_label_when_needed",
            "session_event_log",
        ],
        "required_files": [
            ".agents/skills/dissertation-research-search-protocol/SKILL.md",
            ".agents/skills/dissertation-citation-audit/SKILL.md",
            "knowledge-base/SOURCE_REGISTER.md",
            "knowledge-base/SOURCE_READINESS_MATRIX.md",
        ],
        "receipt_requirements": BOUNDED_RESEARCH_LOOKUP_RECEIPTS,
    },
    {
        "name": "minor_edit",
        "patterns": [
            r"\bminor edit\b",
            r"\btypo\b",
            r"\bpunctuation\b",
            r"\bcitation[- ]key\b",
            r"\breference[- ]format(?:ting)?\b",
            r"\bcitation[- ]format(?:ting)?\b",
            r"\bfix\b.*\b(reference|citation|typo|punctuation)\b",
            r"\b(reference|citation|typo|punctuation)\b.*\bfix\b",
            r"(错字|标点|小修|小改|引用键|引用格式|参考文献格式)",
        ],
        "mode": "Minor Edit Mode",
        "skills": [
            "agent-orchestration",
            "dissertation-source-first-gate",
            "dissertation-citation-audit",
            "context-continuity",
        ],
        "gates": [
            "minor_edit_boundary",
            "no_substantive_prose_change",
            "no_design_or_method_change",
            "no_source_readiness_upgrade",
            "task_state_update_when_substantial",
            "session_event_log_when_substantial",
        ],
        "required_files": [
            ".agents/skills/dissertation-source-first-gate/SKILL.md",
            ".agents/skills/dissertation-citation-audit/SKILL.md",
            "knowledge-base/SOURCE_READINESS_MATRIX.md",
        ],
        "receipt_requirements": MINOR_EDIT_RECEIPTS,
    },
    {
        "name": "authorial_voice_integrity",
        "patterns": [
            r"less\s+AI[- ]?like",
            r"more\s+human",
            r"humanise",
            r"humanize",
            r"de[- ]?AI",
            r"AI[- ]?style",
            r"generic\s+AI",
            r"ChatGPT[- ]?like",
            r"lower\s+AI",
            r"reduce\s+AI",
            r"AI\s+rate",
            r"AIGC",
            r"AI\s+detector",
            r"detection\s+score",
            r"AI[- ]?use\s+disclosure",
            r"AI\s+disclosure",
            r"AI[- ]?use\s+statement",
            r"AI[- ]?generated\s+statement",
            r"(hide|omit|remove|leave out).{0,30}AI\s+statement",
            r"disclosure[- ]?hiding",
            r"去\s*AI",
            r"AI\s*味",
            r"AI\s*率",
            r"降低\s*AI",
            r"降低\s*AIGC",
            r"人工智能.*披露",
            r"AI.*披露",
        ],
        "mode": "Drafting Mode",
        "skills": [
            "agent-orchestration",
            "authorial-voice-integrity",
            "academic-integrity-preflight",
            "academic-self-review-loop",
            "style-fingerprint-gate",
            "uk-academic-writing-style",
            "style-memory-and-revision-gate",
            "dissertation-document-quality-gate",
            "context-continuity",
        ],
        "gates": [
            "authorial_voice_policy",
            "no_detector_evasion_or_score_promise",
            "ai_use_disclosure_boundary",
            "authorial_voice_scan",
            "style_fingerprint_scan",
            "academic_integrity_preflight_when_disclosure_or_prompt_residue_risk",
            "writing_quality_review",
        ],
        "required_files": [
            ".agents/skills/authorial-voice-integrity/SKILL.md",
            ".agents/skills/academic-integrity-preflight/SKILL.md",
            ".agents/skills/academic-self-review-loop/SKILL.md",
            "research-wiki/AI_WRITING_AUTHORIAL_VOICE_POLICY.md",
            "research-wiki/WRITING_QUALITY_RUBRIC.md",
            ".agents/skills/style-fingerprint-gate/SKILL.md",
            "scripts/authorial_voice_scan.py",
            "scripts/style_fingerprint_scan.py",
            "scripts/academic_integrity_preflight.py",
        ],
        "receipt_requirements": [
            "authorial-voice-integrity@writing",
            "style-fingerprint-gate@writing",
            "academic-integrity-preflight@writing",
        ],
    },
    {
        "name": "literature_search",
        "patterns": [r"\bliterature\b", r"文献", r"\bdatabase\b", r"数据库", r"\bsearch\b", r"检索"],
        "mode": "Research Mode",
        "skills": [
            "agent-orchestration",
            "research-project-adapter",
            "dissertation-research-search-protocol",
            "dissertation-learning-loop",
            "dissertation-literature-review",
            "cognitive-frameworks",
            "dissertation-citation-audit",
            "context-continuity",
        ],
        "gates": [
            "research_search_protocol",
            "metadata_only_boundary",
            "source_readiness_update",
            "cognitive_protocol_when_synthesising",
            "learning_loop_update",
        ],
        "required_files": [
            "research-wiki/EXTERNAL_RESEARCH_CONNECTOR_SPEC.md",
            "knowledge-base/SOURCE_REGISTER.md",
            "knowledge-base/SOURCE_READINESS_MATRIX.md",
        ],
        "receipt_requirements": [
            "dissertation-research-search-protocol@research",
            "dissertation-learning-loop@integration",
        ],
    },
    {
        "name": "citation_claim_support",
        "patterns": [r"citation", r"引用", r"claim", r"支持", r"reference", r"参考文献"],
        "mode": "Review Mode",
        "skills": [
            "agent-orchestration",
            "dissertation-citation-audit",
            "dissertation-source-first-gate",
            "context-continuity",
        ],
        "gates": [
            "citation_consistency_check",
            "claim_support_audit",
            "source_readiness_boundary",
            "claim_ledger_lite_when_formal_claims_or_citation_heavy",
        ],
        "required_files": [
            "knowledge-base/SOURCE_READINESS_MATRIX.md",
            "knowledge-base/SOURCE_REGISTER.md",
            "research-wiki/ZOTERO_AND_CITATION_WORKFLOW_SPEC.md",
            *CLAIM_LEDGER_LITE_FILES,
        ],
        "receipt_requirements": [
            "dissertation-citation-audit@review",
        ],
    },
    {
        "name": "requirements_or_rubric",
        "patterns": [
            r"75\+",
            r"(?:assessment|marking|grading|grade|school|university|module|journal|funder|grant|client|submission)\s+rubric",
            r"rubric\s+(?:criteria|band|grade|mark|requirement|evidence|source)",
            r"评分",
            r"marking",
            r"Canvas",
            r"deadline",
            r"word count",
            r"journal",
            r"funder",
            r"grant rule",
            r"client requirement",
            r"submission rule",
            r"author guideline",
        ],
        "mode": "Review Mode",
        "skills": [
            "agent-orchestration",
            "research-project-adapter",
            "dissertation-source-first-gate",
            "dissertation-research-search-protocol",
            "dissertation-research-review",
            "dissertation-document-quality-gate",
        ],
        "gates": [
            "requirement_evidence_gate",
            "source_level_label",
            "no_official_wording_or_requirement_overclaim",
        ],
        "required_files": [
            "compliance/PROJECT_COMPLIANCE_TRACKER.md",
            "quality-gates/PROJECT_DELIVERY_REVIEW_GATE.md",
            "university-guidance/RUBRIC_EVIDENCE_GATE.md",
            "university-guidance/RUBRIC_OR_MARKING_CRITERIA_TEMPLATE.md",
            "university-guidance/MODULE_REQUIREMENTS_TEMPLATE.md",
        ],
        "receipt_requirements": [
            "dissertation-source-first-gate@review",
            "dissertation-document-quality-gate@review",
        ],
    },
    {
        "name": "knowledge_base_operations",
        "patterns": [
            r"knowledge[- ]base",
            r"knowledge base",
            r"self[- ]growing",
            r"\bRAG\b",
            r"retrieval",
            r"vector",
            r"embedding",
            r"Obsidian",
            r"compiled[- ]wiki",
            r"growth[- ]queue",
            r"知识库",
            r"检索",
            r"向量",
        ],
        "mode": "Integration Mode",
        "skills": [
            "agent-orchestration",
            "dissertation-knowledge-ops",
            "dissertation-source-first-gate",
            "context-continuity",
        ],
        "gates": [
            "knowledge_base_privacy_boundary",
            "source_of_record_boundary",
            "retrieval_not_evidence_boundary",
            "kb_health_check",
        ],
        "required_files": [
            "knowledge-base/self-growing/README.md",
            "knowledge-base/self-growing/growth-queue.md",
            "knowledge-base/self-growing/compiled-wiki/INDEX.md",
            "research-wiki/RETRIEVAL_PROTOCOL.md",
            "scripts/kb_health_check.py",
            "scripts/build_agent_index.py",
            "scripts/local_retrieval_search.py",
        ],
        "optional_files": [
            "scripts/build_vector_index.py",
            "scripts/vector_retrieval_smoke_test.py",
            "requirements-vector.txt",
        ],
        "receipt_requirements": [
            "dissertation-knowledge-ops@integration",
        ],
    },
    {
        "name": "system_maintenance",
        "patterns": [
            r"agent",
            r"系统",
            r"bug",
            r"维护",
            r"runtime",
            r"routing",
            r"enforcement",
            r"hard",
            r"starter kit",
            r"template",
            r"generalise",
            r"generalize",
            r"adapt",
            r"profile",
            r"github",
            r"workflow",
            r"rule",
            r"\baudit\b",
            r"\bcontext\s+refresh\b",
            r"\bskill\b.*\b(migration|route|routing|update|audit|stocktake)\b",
            r"\b(migration|route|routing|update|audit|stocktake)\b.*\bskill\b",
            r"\bmigration\b",
            r"\bProduction\s+Window\b",
        ],
        "mode": "Maintenance Mode",
        "skills": [
            "agent-orchestration",
            "research-project-adapter",
            "dissertation-agent-self-debug",
            "dissertation-agent-architecture-audit",
            "dissertation-workspace-surface-audit",
            "context-continuity",
        ],
        "gates": [
            "architecture_audit",
            "tool_state_check",
            "task_state_update",
            "session_event_log",
        ],
        "required_files": [
            "research-wiki/PRODUCTION_RUN_REGISTER.md",
            "research-wiki/PRODUCTION_RECEIPT_VALIDATION.md",
        ],
        "receipt_requirements": [
            "dissertation-agent-self-debug@maintenance",
        ],
    },
]

MAINTENANCE_HINT_PATTERNS = [
    r"\baudit\b",
    r"\bautomation\b",
    r"\bcheck\b",
    r"\bcron\b",
    r"\bimplement\b",
    r"\bprompt\b",
    r"\bupgrade\b",
    r"\bcontext\s+refresh\b",
    r"\bmigration\b",
    r"\bstarter kit\b",
    r"\btemplate\b",
    r"\bgeneralise\b",
    r"\bgeneralize\b",
    r"\badapt\b",
    r"\bgithub\b",
    r"\bupdate\b.*\bskill\b",
    r"\bskill\b.*\b(migration|route|routing|update|audit|stocktake)\b",
    r"\b(migration|route|routing|update|audit|stocktake)\b.*\bskill\b",
    r"\bProduction\s+Window\b",
    r"\bMaintenance\s+Window\b",
    r"\bworkflow\b",
    r"\bcheckpoint\b",
    r"\bself-review\b",
    r"检查",
    r"系统",
    r"维护",
    r"迭代",
    r"升级",
    r"技能",
    r"规则",
]

MAINTENANCE_ONLY_PATTERNS = [
    r"\bautomation\b.*\b(prompt|config|setting|schedule|toml|update)\b",
    r"\b(prompt|config|setting|schedule|toml|update)\b.*\bautomation\b",
    r"\bcron\b.*\b(prompt|config|setting|schedule|toml|update)\b",
    r"\b(prompt|config|setting|schedule|toml|update)\b.*\bcron\b",
    r"自动化.*(提示词|配置|设置|日程|更新)",
    r"(提示词|配置|设置|日程|更新).*自动化",
]

BOUNDED_PLANNING_TERMS = [
    r"\bplan(ning)?\b",
    r"\bpriorit(y|ies)\b",
    r"\bsort\b",
    r"\borganis(e|ation|ing)\b",
    r"\borganiz(e|ation|ing)\b",
    r"\bhierarchy\b",
    r"\brematch\b",
    r"\bsource\s+application\b",
    r"\bsupport\s+audit\b",
    r"计划|规划|准备度|优先|排序|整理|层级|重匹配|应用|支持审计",
]

FORMAL_TEXT_OUTPUT_PATTERNS = [
    r"\b(write|draft|rewrite|redraft|translate|produce|generate|create)\b.*\b(paragraph|section|chapter|draft|proposal|methodology section|literature review|formal|submission|stakeholder[- ]facing|supervisor[- ]facing|reviewer[- ]facing|client[- ]facing|docx|word|report|manuscript|grant)\b",
    r"\b(paragraph|section|chapter|draft|proposal|methodology section|literature review|formal|submission|stakeholder[- ]facing|supervisor[- ]facing|reviewer[- ]facing|client[- ]facing|docx|word|report|manuscript|grant)\b.*\b(write|draft|rewrite|redraft|translate|produce|generate|create)\b",
    r"\bformal\s+(writing|document|draft|output)\b",
    r"\bsubmission[- ]?(facing|ready)?\b",
    r"\b(stakeholder|supervisor|reviewer|client)[- ]facing\b",
    r"\bWord\b",
    r"\bdocx\b",
    r"写.*(段|段落|章节|正文|正式|导师|客户|评审|文档|方法章节|文献综述|总结|报告)",
    r"(撰写|生成|产出|改写|重写|翻译).*(段|段落|章节|正文|正式|导师|客户|评审|文档|方法章节|文献综述|总结|报告)",
    r"(段|段落|章节|正文|正式|导师|客户|评审|文档|方法章节|文献综述|总结|报告).*(写|撰写|生成|产出|改写|重写|翻译)",
]

PROTECTED_SOURCE_OF_RECORD_EDIT_PATTERNS = [
    r"\b(update|edit|modify|change|revise)\b.*\b(SOURCE_REGISTER|SOURCE_READINESS_MATRIX|TASK_STATE|PRODUCTION_RUN_REGISTER|source register|source readiness matrix)\b",
    r"\b(SOURCE_REGISTER|SOURCE_READINESS_MATRIX|TASK_STATE|PRODUCTION_RUN_REGISTER|source register|source readiness matrix)\b.*\b(update|edit|modify|change|revise)\b",
    r"(更新|修改|改动).*(SOURCE_REGISTER|SOURCE_READINESS_MATRIX|TASK_STATE|PRODUCTION_RUN_REGISTER|源登记|准备度矩阵)",
]

PROTECTED_DOCUMENT_PATTERNS = [
    r"\b(final|accepted|approved|locked|official|submission[- ]ready|for submission)\b.*\b(document|draft|report|manuscript|proposal|docx|word|file)\b",
    r"\b(document|draft|report|manuscript|proposal|docx|word|file)\b.*\b(final|accepted|approved|locked|official|submission[- ]ready|for submission)\b",
    r"(最终|已接受|已批准|锁定|正式|提交版|定稿).*(文档|草稿|报告|手稿|proposal|docx|word|文件)",
    r"(文档|草稿|报告|手稿|proposal|docx|word|文件).*(最终|已接受|已批准|锁定|正式|提交版|定稿)",
]

NO_CONTENT_CHANGE_PATTERNS = [
    r"\bdo not change (?:wording|meaning|content|claims?|argument)\b",
    r"\bno (?:wording|meaning|content|claim|argument) change\b",
    r"\bwithout changing (?:wording|meaning|content|claims?|argument)\b",
    r"不(改|修改|改变).*(措辞|含义|内容|claim|论证|正文)",
    r"不动.*(正文|内容|含义|论证)",
]

LOW_COST_EDIT_PATTERNS = [
    r"\bcitation[- ]key\b",
    r"\breference[- ]format(?:ting)?\b",
    r"\bcitation[- ]format(?:ting)?\b",
    r"\btypo\b",
    r"\bpunctuation\b",
]


@dataclass
class RuntimeRoute:
    run_id: str
    timestamp: str
    window: str
    task: str
    mode: str
    task_types: list[str]
    skills: list[str]
    gates: list[str]
    receipt_requirements: list[str]
    required_files: list[str]
    missing_files: list[str]
    warnings: list[str]
    recall_decision: dict
    status: str


def slugify(text: str) -> str:
    slug = re.sub(r"[^A-Za-z0-9]+", "-", text.strip().lower()).strip("-")
    return slug[:48] or "task"


def unique(items: list[str]) -> list[str]:
    seen: set[str] = set()
    output: list[str] = []
    for item in items:
        if item not in seen:
            output.append(item)
            seen.add(item)
    return output


def matches_any(text: str, patterns: list[str]) -> bool:
    return any(re.search(pattern, text, flags=re.I) for pattern in patterns)


def has_bounded_planning_intent(task: str) -> bool:
    return matches_any(task, BOUNDED_PLANNING_TERMS)


def edits_protected_source_of_record(task: str) -> bool:
    return matches_any(task, PROTECTED_SOURCE_OF_RECORD_EDIT_PATTERNS)


def touches_protected_document(task: str) -> bool:
    return matches_any(task, PROTECTED_DOCUMENT_PATTERNS)


def is_no_content_minor_edit(task: str) -> bool:
    return matches_any(task, LOW_COST_EDIT_PATTERNS) and (
        matches_any(task, NO_CONTENT_CHANGE_PATTERNS) or matches_any(task, [r"\bminor\b", r"\bonly\b", r"只", r"小修"])
    )


def has_formal_output_intent(task: str) -> bool:
    if is_no_content_minor_edit(task) and not touches_protected_document(task):
        return False
    if touches_protected_document(task):
        return True
    if matches_any(task, FORMAL_TEXT_OUTPUT_PATTERNS):
        bounded = has_bounded_planning_intent(task)
        hard_formal = matches_any(
            task,
            [
                r"\b(paragraph|section|chapter|draft|formal|submission|stakeholder[- ]facing|supervisor[- ]facing|reviewer[- ]facing|client[- ]facing|docx|word)\b",
                r"(段|段落|章节|正文|正式|导师|客户|评审|文档|Word)",
            ],
        )
        return hard_formal or not bounded
    return False


def classify(task: str, window: str) -> RuntimeRoute:
    matched = []
    for rule in TASK_RULES:
        if any(re.search(pattern, task, flags=re.I) for pattern in rule["patterns"]):
            matched.append(rule)
    formal_rule = next(rule for rule in TASK_RULES if rule["name"] == "formal_research_output")
    bounded_source_rule = next(rule for rule in TASK_RULES if rule["name"] == "bounded_source_planning")
    bounded_lookup_rule = next(rule for rule in TASK_RULES if rule["name"] == "bounded_research_lookup")
    minor_edit_rule = next(rule for rule in TASK_RULES if rule["name"] == "minor_edit")
    formal_output = has_formal_output_intent(task)
    protected_source_edit = edits_protected_source_of_record(task)
    if formal_output and formal_rule not in matched:
        matched.append(formal_rule)
    # Precedence rule: in the Maintenance Window, explicit audit/system/skill
    # wording makes `system_maintenance` the lead route. Other genuinely matched
    # task types can remain as secondary context, but they should not change the
    # overall mode away from Maintenance. Automation config/prompt updates are
    # Maintenance-only because they edit the agent system rather than performing
    # the research task named in the automation.
    if window.lower() == "maintenance" and any(re.search(pattern, task, flags=re.I) for pattern in MAINTENANCE_HINT_PATTERNS):
        system_rule = next(rule for rule in TASK_RULES if rule["name"] == "system_maintenance")
        if any(re.search(pattern, task, flags=re.I) for pattern in MAINTENANCE_ONLY_PATTERNS):
            matched = [system_rule]
        elif system_rule not in matched:
            matched.insert(0, system_rule)
        else:
            matched = [system_rule] + [rule for rule in matched if rule is not system_rule]
    if not matched:
        matched = [TASK_RULES[-1] if window.lower() == "maintenance" else TASK_RULES[0]]

    if protected_source_edit:
        matched = [
            rule
            for rule in matched
            if rule["name"] not in {"bounded_source_planning", "bounded_research_lookup", "minor_edit"}
        ]

    if formal_output:
        matched = [
            rule
            for rule in matched
            if rule["name"] not in {"bounded_source_planning", "bounded_research_lookup", "minor_edit"}
        ]
    elif minor_edit_rule in matched:
        matched = [minor_edit_rule] + [
            rule for rule in matched if rule is not minor_edit_rule and rule["name"] == "system_maintenance"
        ]
    elif bounded_lookup_rule in matched:
        matched = [bounded_lookup_rule] + [
            rule for rule in matched if rule is not bounded_lookup_rule and rule["name"] == "system_maintenance"
        ]
    elif bounded_source_rule in matched:
        matched = [bounded_source_rule] + [
            rule for rule in matched if rule is not bounded_source_rule and rule["name"] == "system_maintenance"
        ]

    if not matched:
        matched = [TASK_RULES[-1] if window.lower() == "maintenance" else formal_rule]

    mode = (
        "Maintenance Mode"
        if window.lower() == "maintenance" and any(r["name"] == "system_maintenance" for r in matched)
        else matched[0]["mode"]
    )
    task_types = [rule["name"] for rule in matched]
    skills = unique([skill for rule in matched for skill in rule["skills"]])
    gates = unique([gate for rule in matched for gate in rule["gates"]])
    receipt_requirements = unique([item for rule in matched for item in rule.get("receipt_requirements", [])])
    task_types = [rule["name"] for rule in matched]
    light_only = bool(task_types) and set(task_types).issubset(LIGHT_TASK_TYPES)
    base_files = LIGHT_BASE_FILES if light_only else BASE_FILES
    required_files = unique(base_files + [path for rule in matched for path in rule["required_files"]])
    recall = decide_stage_recall(task=task, change_type="unspecified")
    if recall.tier >= 3:
        skills = unique(skills + ["context-continuity", "cognitive-frameworks"])
        gates = unique(
            gates
            + [
                "stage_continuity_gate",
                "stage_continuity_capsule_check",
                "deep_reasoning_pass_when_non_obvious",
            ]
        )
        receipt_requirements = unique(receipt_requirements + ["context-continuity@thinking"])
        required_files = unique(
            required_files
            + [
                "research-wiki/STAGE_GRAPH.md",
                "research-wiki/STAGE_CONTINUITY_PROTOCOL.md",
                "scripts/stage_recall_policy.py",
                "scripts/stage_continuity_capsule_check.py",
            ]
        )
    missing_files = [path for path in required_files if not (ROOT / path).exists()]
    warnings = []

    if window.lower() == "maintenance" and any(rule["mode"] == "Drafting Mode" for rule in matched) and not any(
        rule["name"] == "system_maintenance" for rule in matched
    ):
        warnings.append("Task looks like Production drafting but window is Maintenance; confirm window role before drafting.")
    if "requirements_or_rubric" in task_types and "quality-gates/PROJECT_DELIVERY_REVIEW_GATE.md" not in required_files:
        warnings.append("Requirement/rubric task lacks project delivery gate.")
    if "formal_research_output" in task_types and "project_delivery_review_gate" not in gates:
        warnings.append("Formal output lacks project delivery review gate.")
    if "formal_research_output" in task_types and "academic-self-review-loop" not in skills:
        warnings.append("Formal output lacks academic self-review loop.")
    if "formal_research_output" in task_types and "style-fingerprint-gate" not in skills:
        warnings.append("Formal output lacks style fingerprint gate.")
    if "formal_research_output" in task_types and "skill_execution_receipts_for_required_gates" not in gates:
        warnings.append("Formal output lacks skill execution receipt gate.")
    if "authorial_voice_integrity" in task_types and "authorial-voice-integrity" not in skills:
        warnings.append("Authorial voice task lacks authorial voice integrity skill.")
    if "authorial_voice_integrity" in task_types and "authorial_voice_scan" not in gates:
        warnings.append("Authorial voice task lacks authorial voice scan gate.")
    if "formal_research_output" in task_types and "material-passport" not in skills:
        warnings.append("Formal output lacks Material Passport.")
    if "formal_research_output" in task_types and "formal-delivery-guard" not in skills:
        warnings.append("Formal output lacks formal delivery guard.")
    if "formal_research_output" in task_types and not {
        "thinking_checkpoint",
        "writing_checkpoint",
        "delivery_checkpoint_when_delivering_docx",
        "material_passport",
    }.issubset(set(gates)):
        warnings.append("Formal output lacks staged checkpoint gates.")
    if recall.tier == 4:
        warnings.append("Recall tier 4: pause for branch decision or run full upstream audit only when explicitly requested.")

    status = "PASS" if not missing_files and not any("lacks" in warning for warning in warnings) else "BLOCKED"
    timestamp = datetime.now().isoformat(timespec="seconds")
    return RuntimeRoute(
        run_id=f"{datetime.now().strftime('%Y-%m-%d')}-{slugify(task)}",
        timestamp=timestamp,
        window=window,
        task=task,
        mode=mode,
        task_types=task_types,
        skills=skills,
        gates=gates,
        receipt_requirements=receipt_requirements,
        required_files=required_files,
        missing_files=missing_files,
        warnings=warnings,
        recall_decision=asdict(recall),
        status=status,
    )


def append_event(route: RuntimeRoute, event_type: str, status: str, evidence: str, risk: str = "low") -> None:
    EVENT_LOG.parent.mkdir(parents=True, exist_ok=True)
    event = {
        "timestamp": route.timestamp,
        "run_id": route.run_id,
        "window": route.window,
        "event_type": event_type,
        "status": status,
        "skill": "agent-runtime-enforcement",
        "file": "scripts/agent_runtime.py",
        "evidence": evidence,
        "risk": risk,
    }
    with EVENT_LOG.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(event, ensure_ascii=False) + "\n")


def model_label() -> tuple[str, str]:
    for key in ("CODEX_MODEL", "OPENAI_MODEL", "MODEL", "GPT_MODEL"):
        value = os.environ.get(key)
        if value:
            return value, f"env:{key}"
    return "unknown", "not_exposed_to_runtime"


def required_file_bytes(paths: list[str]) -> int:
    total = 0
    for rel_path in paths:
        path = ROOT / rel_path
        if path.exists() and path.is_file():
            total += path.stat().st_size
    return total


def append_context_health_signal(route: RuntimeRoute, runtime_receipt: Path | None = None) -> None:
    model, model_source = model_label()
    bytes_total = required_file_bytes(route.required_files)
    signal = {
        "schema": "context_health_signal.v1",
        "timestamp": route.timestamp,
        "source": "runtime_preflight",
        "run_id": route.run_id,
        "window": route.window,
        "task": route.task,
        "mode": route.mode,
        "task_types": route.task_types,
        "model": model,
        "model_source": model_source,
        "turn_count": None,
        "turn_count_source": "not_exposed_to_runtime",
        "context_compressed": "unknown",
        "context_compressed_source": "not_exposed_to_runtime",
        "approx_input_tokens": None,
        "approx_output_tokens": None,
        "approx_total_tokens": None,
        "token_scale": "unknown",
        "symptom": "runtime preflight route signal",
        "severity": "info",
        "recall_tier": route.recall_decision.get("tier"),
        "recall_tier_name": route.recall_decision.get("tier_name"),
        "required_file_count": len(route.required_files),
        "required_file_bytes": bytes_total,
        "skills_count": len(route.skills),
        "gates_count": len(route.gates),
        "receipt_requirement_count": len(route.receipt_requirements),
        "runtime_receipt_json": str(runtime_receipt.relative_to(ROOT)) if runtime_receipt else None,
    }
    CONTEXT_HEALTH_LOG.parent.mkdir(parents=True, exist_ok=True)
    with CONTEXT_HEALTH_LOG.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(signal, ensure_ascii=False) + "\n")


def markdown(route: RuntimeRoute) -> str:
    lines = [
        "# Agent Runtime Preflight",
        "",
        f"Generated: {route.timestamp}",
        f"Run ID: `{route.run_id}`",
        f"Window: `{route.window}`",
        f"Status: `{route.status}`",
        "",
        "## Task",
        "",
        route.task,
        "",
        "## Deterministic Routing",
        "",
        f"- Mode: {route.mode}",
        f"- Task types: {', '.join(route.task_types)}",
        f"- Skills: {', '.join(route.skills)}",
        f"- Gates: {', '.join(route.gates)}",
        "",
        "## Recall Decision",
        "",
        f"- Tier: {route.recall_decision.get('tier')} ({route.recall_decision.get('tier_name')})",
        f"- Recommended action: {route.recall_decision.get('recommended_action')}",
        f"- Floor reasons: {', '.join(route.recall_decision.get('floor_reasons', []))}",
        "",
        "## Required Skill Execution Receipts",
        "",
    ]
    lines.extend(f"- `{item}`" for item in route.receipt_requirements) if route.receipt_requirements else lines.append("- None")
    lines.extend(
        [
            "",
            "## Required Files",
            "",
        ]
    )
    lines.extend(f"- `{path}`" for path in route.required_files)
    lines.extend(["", "## Missing Files", ""])
    lines.extend(f"- `{path}`" for path in route.missing_files) if route.missing_files else lines.append("- None")
    lines.extend(["", "## Warnings", ""])
    lines.extend(f"- {warning}" for warning in route.warnings) if route.warnings else lines.append("- None")
    lines.extend(
        [
            "",
            "## Boundary",
            "",
            "This is a deterministic local preflight. It hard-checks routing, required gates, and required files, but it does not perform the research task itself.",
        ]
    )
    return "\n".join(lines) + "\n"


def write_receipts(route: RuntimeRoute) -> tuple[Path, Path]:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")
    json_path = OUT_DIR / f"runtime_preflight_{stamp}_{slugify(route.task)}.json"
    md_path = OUT_DIR / f"runtime_preflight_{stamp}_{slugify(route.task)}.md"
    json_path.write_text(json.dumps(asdict(route), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    md_path.write_text(markdown(route), encoding="utf-8")
    return json_path, md_path


def main() -> int:
    parser = argparse.ArgumentParser(description="Run deterministic research-agent routing preflight.")
    parser.add_argument("task", help="User task or short task description.")
    parser.add_argument("--window", choices=["Production", "Maintenance"], default="Maintenance")
    parser.add_argument("--write", action="store_true", help="Write JSON/Markdown receipts and append a session event.")
    parser.add_argument("--strict", action="store_true", help="Return non-zero when status is BLOCKED.")
    args = parser.parse_args()

    route = classify(args.task, args.window)
    print(json.dumps(asdict(route), ensure_ascii=False, indent=2))
    if args.write:
        json_path, md_path = write_receipts(route)
        append_context_health_signal(route, json_path)
        append_event(
            route,
            "session_start",
            "completed" if route.status == "PASS" else "blocked",
            "Runtime preflight started a routed task session.",
            "low" if route.status == "PASS" else "medium",
        )
        append_event(
            route,
            "gate_completed",
            "completed" if route.status == "PASS" else "failed",
            f"Runtime preflight wrote {json_path.relative_to(ROOT)} and {md_path.relative_to(ROOT)}.",
            "low" if route.status == "PASS" else "medium",
        )
        append_event(
            route,
            "session_end",
            "completed" if route.status == "PASS" else "blocked",
            "Runtime preflight completed local routing and required-file checks.",
            "low" if route.status == "PASS" else "medium",
        )
        print(f"JSON receipt: {json_path}")
        print(f"Markdown receipt: {md_path}")
    return 1 if args.strict and route.status != "PASS" else 0


if __name__ == "__main__":
    raise SystemExit(main())
