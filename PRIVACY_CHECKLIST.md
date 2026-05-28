# Privacy Checklist

Run this before each push or before giving access to another person.

## Must Not Be Included

- real student name, email, ID, signature
- supervisor name or private feedback
- university login URLs that reveal private course access
- Canvas screenshots or copied restricted module content
- ethics forms with personal details
- participant-facing forms with real personal details unless intentionally shared
- interview recordings, transcripts, raw notes, participant quotes
- consent forms or withdrawal forms
- API keys, tokens, cookies, `.env` files
- browser profiles or local app session files
- assessed dissertation drafts unless the repository is private and intentionally shared

## Safe To Include

- generic agent skills
- generic workflow rules
- source-first and quality-gate rules
- blank templates
- anonymised examples
- public URLs
- bibliographic metadata for public or library sources

## Before Push

1. Run `scripts/privacy_check.sh`.
2. Search manually for names, emails, institution-specific private details, and participant identifiers.
3. Check `git status`.
4. Stage only intended files.
5. Commit with a clear message.
6. Push only to a private repository unless the repository has been fully public-audited.

## Before Public Release

Complete `PUBLIC_RELEASE_AUDIT.md`.
