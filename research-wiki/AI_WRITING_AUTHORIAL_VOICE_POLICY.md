# AI Writing And Authorial Voice Policy

Last updated: 2026-06-02

## Purpose

Define how this starter kit handles requests framed as AI writing, AI-looking prose, de-AI, humanising, AIGC, AI detector scores, or AI-use disclosure.

The system does not optimise for detector scores. It improves authorial voice, argument quality, academic or professional integrity, and evidence-led prose.

## Core Position

Allowed:

- remove prompt residue, chatbot meta-text, placeholders, and generic AI-style phrasing;
- strengthen paragraph-level judgement through clearer mini-claims, warrants, and evidence boundaries;
- improve project-appropriate register, including UK academic style when the project context requires it;
- preserve meaning, citations, dates, names, participant facts, official requirements, and source boundaries;
- explain what changed and why.

Not allowed:

- promise lower AI-detection, AIGC-detection, Turnitin, GPTZero, or platform-detection scores;
- use detector evasion, randomness injection, synonym-swap evasion, stylistic-noise insertion, or deliberate imperfection as a workflow goal;
- promise how detectors, assessors, reviewers, readers, or platforms will perceive authorship;
- hide unsupported claims through smoother wording;
- rewrite references, evidence, ethics/compliance statements, official requirements, or personal/admin facts for style;
- hide, soften, remove, or invent AI-use disclosure statements;
- make claims about institutional AI-use disclosure rules without checking local evidence first.

## Default Workflow

For formal academic or professional prose:

1. Source-first check and Material Passport when formal claims are involved.
2. `academic-integrity-preflight`.
3. `cognitive-frameworks`.
4. `academic-self-review-loop`.
5. `authorial-voice-integrity` and `scripts/authorial_voice_scan.py` when style/integrity risk matters.
6. Project style gate, such as `uk-academic-writing-style` for UK academic work.
7. `style-memory-and-revision-gate`.
8. Document-quality and formal delivery gates when delivering artifacts.

For quick chat answers, do not run the full pipeline. Apply the same boundary in concise form: improve clarity and authorial voice, do not promise detector outcomes.

## Ownership

Canonical skill:

- `authorial-voice-integrity` owns AI-writing, de-AI, humanising, detector-framed, and disclosure-risk writing requests.

Supporting gates:

- `academic-integrity-preflight` owns prompt residue, placeholders, fake references, unsupported claims, and misleading disclosure.
- `academic-self-review-loop` owns paragraph quality, warrants, and argument progression.
- `uk-academic-writing-style` or the confirmed project style skill owns academic register.
- `style-memory-and-revision-gate` owns user-facing answer shape and revision accountability.

## Authorial Voice Checks

Check whether the text:

- opens paragraphs with a specific mini-claim rather than broad setup;
- uses evidence as part of the sentence logic, not as decoration after a generic claim;
- contains a visible warrant when moving from literature, data, or requirements to interpretation;
- avoids generic AI-style transitions and inflated academic vocabulary;
- keeps uncertainty visible when source support is incomplete;
- removes repeated meta-commentary, symmetrical paragraph patterns, and empty connector sentences;
- preserves the user's substantive judgement rather than replacing it with polished generalities.

## Integrity Boundary

Prompt residue, fake references, placeholders, unsupported claims, misleading AI-use disclosure, and unresolved source markers are not style problems. Route them to `academic-integrity-preflight` before rewriting.

This policy is not a plagiarism detector, AI detector, or official institutional policy. It is a writing-quality and integrity policy.
