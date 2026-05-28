# External Research Connector Spec

Purpose: define safe academic database and metadata search behaviour.

## Active Local Tool

- `scripts/academic_database_connector.py`

## Supported Providers

| Provider | Status | Boundary |
|---|---|---|
| OpenAlex | public metadata search | metadata only |
| Crossref | public metadata search | metadata only |
| Semantic Scholar | public metadata search | metadata only; may rate-limit |
| Scopus | credential-aware connector | requires lawful `ELSEVIER_CREDENTIAL`; entitlement may vary |
| Web of Science | credential-aware connector | requires `WOS_CREDENTIAL` and institution-specific endpoint |
| EBSCO | credential-aware connector | requires institutional endpoint and authentication |

## Rule

Search results are `METADATA ONLY` until relevant source sections have been reviewed and `knowledge-base/SOURCE_READINESS_MATRIX.md` is updated.

Do not scrape restricted databases or store credentials in Git.
