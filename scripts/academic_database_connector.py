#!/usr/bin/env python3
"""Academic database connector with public metadata search and subscription checks.

Subscription providers require institutional credentials. This script will
not scrape restricted databases or store credentials.
"""

from __future__ import annotations

import argparse
import json
import os
import textwrap
import urllib.parse
import urllib.request
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "knowledge-base" / "api-searches"

PUBLIC_PROVIDERS = {"openalex", "crossref", "semantic_scholar"}
SUBSCRIPTION_PROVIDERS = {"scopus", "web_of_science", "ebsco"}


def fetch_json(url: str, headers: dict[str, str] | None = None) -> dict:
    contact = os.environ.get("AGENT_CONTACT_EMAIL", "").strip()
    user_agent = "ResearchAgentStarterKit/1.0"
    if contact:
        user_agent = f"{user_agent} (mailto:{contact})"
    request_headers = {"User-Agent": user_agent, "Accept": "application/json"}
    if headers:
        request_headers.update(headers)
    req = urllib.request.Request(url, headers=request_headers)
    with urllib.request.urlopen(req, timeout=30) as response:
        return json.loads(response.read().decode("utf-8"))


def normalise_result(provider: str, title: str = "", year: str | int = "", authors: str = "", venue: str = "", doi: str = "", url: str = "", abstract: str = "") -> dict:
    return {
        "provider": provider,
        "title": title or "",
        "year": str(year or ""),
        "authors": authors or "",
        "venue": venue or "",
        "doi": (doi or "").replace("https://doi.org/", ""),
        "url": url or "",
        "abstract": abstract or "",
        "evidence_status": "METADATA ONLY",
    }


def search_openalex(query: str, limit: int) -> list[dict]:
    params = urllib.parse.urlencode({"search": query, "per-page": limit})
    data = fetch_json(f"https://api.openalex.org/works?{params}")
    results = []
    for item in data.get("results", []):
        results.append(
            normalise_result(
                "OpenAlex",
                title=item.get("display_name", ""),
                year=item.get("publication_year", ""),
                doi=item.get("doi", ""),
                url=item.get("id", ""),
                venue=(item.get("primary_location") or {}).get("source", {}).get("display_name", ""),
                authors=", ".join(a.get("author", {}).get("display_name", "") for a in item.get("authorships", [])[:6]),
            )
        )
    return results


def search_crossref(query: str, limit: int) -> list[dict]:
    params = urllib.parse.urlencode({"query.bibliographic": query, "rows": limit})
    data = fetch_json(f"https://api.crossref.org/works?{params}")
    results = []
    for item in data.get("message", {}).get("items", []):
        year_parts = item.get("issued", {}).get("date-parts", [[None]])
        authors = []
        for author in item.get("author", [])[:6]:
            name = " ".join(part for part in [author.get("given", ""), author.get("family", "")] if part)
            if name:
                authors.append(name)
        results.append(
            normalise_result(
                "Crossref",
                title="; ".join(item.get("title", [])[:1]),
                year=year_parts[0][0] if year_parts and year_parts[0] else "",
                doi=item.get("DOI", ""),
                url=item.get("URL", ""),
                venue="; ".join(item.get("container-title", [])[:1]),
                authors=", ".join(authors),
            )
        )
    return results


def search_semantic_scholar(query: str, limit: int) -> list[dict]:
    params = urllib.parse.urlencode(
        {
            "query": query,
            "limit": min(limit, 100),
            "fields": "title,authors,year,venue,externalIds,url,abstract",
        }
    )
    headers = {}
    credential = os.environ.get("SEMANTIC_SCHOLAR_CREDENTIAL", "").strip()
    if credential:
        headers["x-api-key"] = credential
    data = fetch_json(f"https://api.semanticscholar.org/graph/v1/paper/search?{params}", headers=headers)
    results = []
    for item in data.get("data", []):
        external = item.get("externalIds") or {}
        results.append(
            normalise_result(
                "Semantic Scholar",
                title=item.get("title", ""),
                year=item.get("year", ""),
                doi=external.get("DOI", ""),
                url=item.get("url", ""),
                venue=item.get("venue", ""),
                authors=", ".join(author.get("name", "") for author in item.get("authors", [])[:6]),
                abstract=item.get("abstract", "") or "",
            )
        )
    return results


def provider_status() -> list[dict]:
    return [
        {
            "provider": "OpenAlex",
            "type": "public metadata",
            "status": "configured",
            "required": "network access",
        },
        {
            "provider": "Crossref",
            "type": "public metadata",
            "status": "configured",
            "required": "network access",
        },
        {
            "provider": "Semantic Scholar",
            "type": "public metadata",
            "status": "configured; optional credential" if os.environ.get("SEMANTIC_SCHOLAR_CREDENTIAL") else "configured without credential",
            "required": "network access; optional SEMANTIC_SCHOLAR_CREDENTIAL",
        },
        {
            "provider": "Scopus",
            "type": "subscription metadata",
            "status": "configured" if os.environ.get("ELSEVIER_CREDENTIAL") else "not configured",
            "required": "ELSEVIER_CREDENTIAL; optional ELSEVIER_INSTTOKEN depending on institutional entitlement",
        },
        {
            "provider": "Web of Science",
            "type": "subscription metadata",
            "status": "configured" if os.environ.get("WOS_CREDENTIAL") and os.environ.get("WOS_ENDPOINT") else "not configured",
            "required": "WOS_CREDENTIAL and WOS_ENDPOINT for the institution's subscribed product",
        },
        {
            "provider": "EBSCO",
            "type": "subscription discovery",
            "status": "configured" if os.environ.get("EBSCO_ENDPOINT") and (os.environ.get("EBSCO_CREDENTIAL") or os.environ.get("EBSCO_USER")) else "not configured",
            "required": "EBSCO_ENDPOINT and either EBSCO_CREDENTIAL or institutional user credentials",
        },
    ]


def search_scopus(query: str, limit: int) -> list[dict]:
    credential = os.environ.get("ELSEVIER_CREDENTIAL", "").strip()
    if not credential:
        raise RuntimeError("Scopus is not configured: missing ELSEVIER_CREDENTIAL.")
    params = urllib.parse.urlencode({"query": query, "count": min(limit, 25), "httpAccept": "application/json"})
    headers = {"X-ELS-APIKey": credential}
    insttoken = os.environ.get("ELSEVIER_INSTTOKEN", "").strip()
    if insttoken:
        headers["X-ELS-Insttoken"] = insttoken
    data = fetch_json(f"https://api.elsevier.com/content/search/scopus?{params}", headers=headers)
    results = []
    for item in data.get("search-results", {}).get("entry", []):
        results.append(
            normalise_result(
                "Scopus",
                title=item.get("dc:title", ""),
                year=(item.get("prism:coverDate", "") or "")[:4],
                doi=item.get("prism:doi", ""),
                url=item.get("prism:url", ""),
                venue=item.get("prism:publicationName", ""),
                authors=item.get("dc:creator", ""),
            )
        )
    return results


def unsupported_subscription_search(provider: str) -> list[dict]:
    raise RuntimeError(
        f"{provider} requires institution-specific endpoint/authentication configuration. "
        "Use the status command and create a local/private connector config or environment variables first."
    )


def run_search(query: str, providers: list[str], limit: int) -> tuple[list[dict], list[str]]:
    results: list[dict] = []
    errors: list[str] = []
    for provider in providers:
        try:
            if provider == "openalex":
                results.extend(search_openalex(query, limit))
            elif provider == "crossref":
                results.extend(search_crossref(query, limit))
            elif provider == "semantic_scholar":
                results.extend(search_semantic_scholar(query, limit))
            elif provider == "scopus":
                results.extend(search_scopus(query, limit))
            elif provider in {"web_of_science", "ebsco"}:
                unsupported_subscription_search(provider)
            else:
                errors.append(f"Unknown provider: {provider}")
        except Exception as exc:  # noqa: BLE001 - report connector failures without hiding them
            errors.append(f"{provider}: {exc}")
    return results, errors


def render_status() -> str:
    lines = [
        "# Academic Database Connector Status",
        "",
        f"Generated: {datetime.now().isoformat(timespec='seconds')}",
        "",
        "| Provider | Type | Status | Required configuration |",
        "|---|---|---|---|",
    ]
    for item in provider_status():
        lines.append(f"| {item['provider']} | {item['type']} | {item['status']} | {item['required']} |")
    lines.extend(
        [
            "",
            "## Boundary",
            "",
        "Public providers return metadata only. Subscription providers need lawful institutional credentials. This tool does not scrape restricted databases or store credentials.",
        ]
    )
    return "\n".join(lines) + "\n"


def render_search(query: str, providers: list[str], results: list[dict], errors: list[str]) -> str:
    lines = [
        "# Academic Database Search",
        "",
        f"Generated: {datetime.now().isoformat(timespec='seconds')}",
        f"Query: `{query}`",
        f"Providers: {', '.join(providers)}",
        "",
        "Evidence status: `METADATA ONLY`.",
        "",
        "| Provider | Title | Year | Authors | Venue | DOI/URL |",
        "|---|---|---:|---|---|---|",
    ]
    for item in results:
        title = item["title"].replace("|", "\\|")
        authors = item["authors"].replace("|", "\\|")
        venue = item["venue"].replace("|", "\\|")
        doi_url = item["doi"] or item["url"]
        lines.append(f"| {item['provider']} | {title} | {item['year']} | {authors} | {venue} | {doi_url} |")
    lines.extend(["", "## Connector Errors / Boundaries", ""])
    lines.extend(f"- {error}" for error in errors) if errors else lines.append("- None")
    lines.extend(
        [
            "",
            "## Use Rule",
            "",
            "Do not cite these records as claim evidence until the relevant source sections have been reviewed and `SOURCE_READINESS_MATRIX.md` is updated.",
        ]
    )
    return "\n".join(lines) + "\n"


def write_report(content: str, stem: str) -> Path:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    path = OUT_DIR / f"{stem}_{datetime.now().strftime('%Y-%m-%d_%H%M%S')}.md"
    path.write_text(content, encoding="utf-8")
    return path


def main() -> int:
    parser = argparse.ArgumentParser(description="Search/check academic database connectors.")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("status", help="Report configured public and subscription database connectors.")
    search = sub.add_parser("search", help="Run a metadata search.")
    search.add_argument("query")
    search.add_argument("--providers", default="openalex,crossref,semantic_scholar")
    search.add_argument("--include-subscription", action="store_true")
    search.add_argument("--limit", type=int, default=10)
    args = parser.parse_args()

    if args.command == "status":
        content = render_status()
        path = write_report(content, "academic_database_connector_status")
        print(f"Report: {path}")
        print(content)
        return 0

    providers = [item.strip() for item in args.providers.split(",") if item.strip()]
    if args.include_subscription:
        providers = list(dict.fromkeys(providers + sorted(SUBSCRIPTION_PROVIDERS)))
    results, errors = run_search(args.query, providers, args.limit)
    slug = "-".join(args.query.lower().split())[:70] or "query"
    path = write_report(render_search(args.query, providers, results, errors), f"academic_database_search_{slug}")
    print(
        textwrap.dedent(
            f"""
            Results: {len(results)}
            Errors/boundaries: {len(errors)}
            Report: {path}
            Evidence status: METADATA ONLY
            """
        ).strip()
    )
    return 0 if results or errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
