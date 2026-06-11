# Homepage Creative Brief

Date: 2026-06-11

Purpose: guide README, GitHub social preview, and optional GitHub Pages design for the public research-agent starter kit.

## Positioning Route

Selected route: **Trust-First Research Cockpit**

Audience:

- Researchers, postgraduate students, research teams, and evidence-heavy writers using coding agents for formal research work.

First-screen promise:

- Local-first research-agent workflows for people who need defensible formal outputs, not just fluent drafts.

Commercial / adoption logic:

- Users should understand within five seconds that this is not another generic AI writing prompt pack. It is a local workflow system that makes source checks, routing decisions, receipts, and delivery blocks auditable.

## Visual Direction

Use:

- clean technical documentation style;
- white or near-white background;
- dark neutral text;
- restrained blue/green accents for pass/check/gate states;
- monospace snippets for runtime examples;
- compact interface fragments showing task routing, source gates, receipts, and delivery guard status.

Avoid:

- generic AI glow, robot, brain, neural-network, or purple-gradient visuals;
- fake dashboards with unreadable text;
- stock academic imagery;
- marketing claims about grades, publication, acceptance, or approval;
- decorative diagrams that do not explain a real workflow.

## Homepage Structure

1. **Hero / README first screen**
   - H1: `Research Agent Starter Kit`
   - One-line outcome promise.
   - One paragraph explaining local-first source checks, light routing, receipts, and delivery blocking.
   - Badges after the promise, not before it.

2. **What It Protects**
   - Short table mapping risks to guards.
   - This should appear before long feature descriptions.

3. **Concrete Routing Example**
   - Show one bounded route and one formal-output route.
   - Use terminal-style examples instead of abstract claims.

4. **How It Works**
   - Keep the Mermaid diagram after the value proposition.
   - Use it as proof, not as the first explanation.

5. **Quick Start + Validation**
   - Validation should remain highly visible because trust is a core differentiator.

## Creative Production Asset Sequence

Recommended order:

1. **GitHub social preview card**
   - 1280 x 640.
   - Typographic, minimal.
   - Copy: `Research Agent Starter Kit` + `Local-first workflows for defensible formal research outputs.`
   - Status: created at `docs/assets/social-preview.png`, with editable source at `docs/assets/social-preview.svg`.
   - Publication note: upload the PNG through GitHub repository settings if GitHub does not expose a stable API-backed social-preview update path.

2. **Annotated terminal demo image**
   - Show `bounded_source_planning` versus `formal_research_output`.
   - This is the highest-trust developer-facing asset.
   - Status: created at `docs/assets/terminal-routing-demo.png`, with editable source at `docs/assets/terminal-routing-demo.svg`.
   - README placement: embedded under the concrete routing example in both `README.md` and `README_CN.md`.

3. **Revised workflow diagram**
   - Narrow the visual story to source gate -> routing -> receipts -> delivery guard.
   - Keep full details in documentation.

4. **Optional GitHub Pages mock**
   - Only after README positioning is stable.
   - One static page, no heavy app shell.

## Copy Guardrails

- Say what the system blocks and records.
- Keep limits visible.
- Do not claim academic correctness, compliance approval, source support, grades, publication, funding, or acceptance.
- Treat validation as workflow coverage, not proof of research quality.
