# Acknowledgements

This project was built through iterative development and draws inspiration from several open-source projects and academic resources.

## Open-Source Inspirations

### Cognitive reasoning frameworks

The cognitive-frameworks skill in this system was inspired by the argumentation reasoning framework, review quality thinking, and writing judgment framework concepts from [Imbad0202/academic-research-skills](https://github.com/Imbad0202/academic-research-skills).

### Rhetorical move sequences

The section-specific rhetorical moves and editorial principles were informed by the research writing patterns documented in [SNL-UCSB/paper-writing-skill](https://github.com/SNL-UCSB/paper-writing-skill), which were extracted from forensic analysis of accepted vs. rejected papers.

### Self-review improvement loop

The academic-self-review-loop skill was inspired by the auto-paper-improvement-loop workflow in [ARIS (Auto-Research-In-Sleep)](https://github.com/wanshuiyin/Auto-claude-code-research-in-sleep), particularly the principle of context-naive reviewing across rounds.

### Academic writing methodology

Writing quality principles were also informed by research paper writing methodologies adapted from Prof. Peng Sida's open notes, as curated in [Master-cai/Research-Paper-Writing-Skills](https://github.com/Master-cai/Research-Paper-Writing-Skills).

## APIs and Services

- [OpenAlex](https://openalex.org/) — Open scholarly metadata
- [Crossref](https://www.crossref.org/) — DOI and citation metadata
- [Semantic Scholar](https://www.semanticscholar.org/) — Academic paper search and citation data
- [Zotero](https://www.zotero.org/) — Reference management

## Tools

- Built to run on [OpenAI Codex CLI](https://github.com/openai/codex) or any compatible LLM agent
- Word document generation via [python-docx](https://python-docx.readthedocs.io/) and [LibreOffice](https://www.libreoffice.org/)
- Vector retrieval via [ChromaDB](https://www.trychroma.com/) and [sentence-transformers](https://www.sbert.net/)
