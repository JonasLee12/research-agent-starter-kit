# GitHub Private Sharing

## Recommended Setup

Use a private GitHub repository.

Invite friends through GitHub repository settings:

```text
Settings -> Collaborators and teams -> Add people
```

Before friends clone the repository, ask them to check:

- [`SOFTWARE_AND_PLUGIN_REQUIREMENTS.md`](SOFTWARE_AND_PLUGIN_REQUIREMENTS.md)
- [`APP_AND_CONNECTOR_USAGE.md`](APP_AND_CONNECTOR_USAGE.md)
- `README.md` or `README_CN.md`, depending on language preference

## Update Workflow

Owner:

```bash
git status
./scripts/privacy_check.sh
git add .
git commit -m "Update research agent template"
git push
```

Friend:

```bash
git pull
```

## Privacy Rule

Keep the repository private unless it has been fully public-audited.

## Current GitHub Status

- Repository name: `research-agent-starter-kit`
- Recommended visibility before final audit: private
- Template repository: yes
- Latest required local tooling note: Python 3 is needed for the included scripts and validation tests; extra Python packages are not required by default.
- Claude Code is optional and should be used only through the privacy-gated review workflow when enabled.
- Neural vector retrieval is optional and requires `requirements-vector.txt`; generated indexes under `.agent-runtime/` should not be committed.
