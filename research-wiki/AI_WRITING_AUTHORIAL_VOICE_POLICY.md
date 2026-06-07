# AI Writing, Academic Integrity, And Authorial Voice Policy

Purpose: route requests about "AI-looking writing", "humanising", "de-AI", AIGC detection, or similar phrasing into legitimate authorial-voice, academic-integrity, and research-writing quality work.

## Core Rule

Allowed:

- improve clarity, paragraph movement, academic register, and discipline-appropriate voice;
- remove prompt residue, generic filler, repeated templates, unsupported certainty, and mechanical transitions;
- help the author state their own judgement, evidence boundary, and source-based reasoning more clearly;
- check whether required AI-use disclosure or coversheet statements need attention, based only on user-provided or project guidance.

Not allowed:

- promise to lower an AI detector score or detection rate;
- rewrite text to bypass Turnitin, GPTZero, AIGC tools, or any authorship detector;
- insert deliberate mistakes, random wording, synonym-swap noise, or artificial imperfection;
- hide, soften, or fabricate AI-use disclosure;
- claim that prose is or is not AI-generated.

## Trigger Phrases

Treat these as authorial-voice / integrity tasks, not detector-evasion tasks:

- "lower AI rate", "reduce AI score", "pass AI detector", "avoid AI detection";
- "humanise", "de-AI", "AI fingerprints", "sounds like AI";
- "降 AI", "降 AIGC", "去 AI 味", "AI 痕迹", "AI 检测率", "绕过检测".

## Required Response Shape

When triggered, say the work will be handled as:

1. academic integrity check;
2. authorial voice and register scan;
3. style-fingerprint scan for repeated templates;
4. targeted revision that preserves claims, citations, uncertainty level, and source boundaries.

Do not use detector-score language in the deliverable.

## Workflow For Formal Research Prose

1. Run or apply `academic-integrity-preflight` first if the request mentions disclosure, AI-use statements, prompt residue, placeholders, fake references, or unsupported claims.
2. Use source-first and Material Passport gates when the text is formal, citation-heavy, or stakeholder-facing.
3. Use `academic-self-review-loop` for argument quality.
4. Run:

```bash
python3 scripts/authorial_voice_scan.py --target <draft> --strict
python3 scripts/style_fingerprint_scan.py <draft> --strict
```

5. Revise only the flagged language issues that weaken readability, register, argument movement, or source-boundary clarity.
6. Re-run the relevant scanners if the revision materially changes the prose.
7. For formal delivery, create skill execution receipts and run the final delivery guard when enabled.

## Authorial Voice Signals To Improve

- repeated stock transitions, such as "This matters because", "Taken together", or "These sources show";
- repeated paragraph-final codas that make different paragraphs end in the same way;
- overused abstract nouns carrying too much of the argument;
- paragraphs that cite sources but do not state the author's judgement;
- long runs of similarly structured claim-because-implication sentences;
- binary negative-contrast templates overused beyond genuine scope distinctions.

## Boundaries

This policy is not an AI detector, plagiarism detector, authorship detector, institutional policy, or official assessment rule. It supports clearer research prose and honest disclosure boundaries only.
