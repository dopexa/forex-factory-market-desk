#!/usr/bin/env python3
"""Build a small, attributed headline feed for the static GitHub Pages site."""

import argparse
import email.utils
import json
import re
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path


QUERIES = (
    "forex OR currency OR currencies",
    "central bank OR Federal Reserve OR ECB interest rates",
    "foreign exchange OR gold OR oil markets",
)
FEED_URL = "https://news.google.com/rss/search"


def clean_text(value):
    return re.sub(r"\s+", " ", value or "").strip()


def parse_items(xml_data):
    root = ET.fromstring(xml_data)
    results = []
    for item in root.findall(".//item"):
        title = clean_text(item.findtext("title"))
        link = clean_text(item.findtext("link"))
        source = clean_text(item.findtext("source")) or "Google News"
        published = clean_text(item.findtext("pubDate"))
        if title.endswith(" - " + source):
            title = title[: -(len(source) + 3)].strip()
        if not title or not link.startswith("https://"):
            continue
        try:
            published_at = email.utils.parsedate_to_datetime(published).astimezone(timezone.utc).isoformat()
        except (TypeError, ValueError, OverflowError):
            published_at = None
        results.append({
            "title": title,
            "source": source,
            "link": link,
            "publishedAt": published_at,
        })
    return results


def fetch_query(query):
    url = FEED_URL + "?" + urllib.parse.urlencode({
        "q": query,
        "hl": "en-US",
        "gl": "US",
        "ceid": "US:en",
    })
    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": "MarketDesk/1.0 (headline reader)",
            "Accept": "application/rss+xml, application/xml, text/xml",
        },
    )
    with urllib.request.urlopen(request, timeout=15) as response:
        return parse_items(response.read())


def build_feed():
    items = []
    for query in QUERIES:
        try:
            items.extend(fetch_query(query))
        except Exception as error:  # Keep publishing if one upstream query is unavailable.
            print(f"Could not fetch one news query: {error}")

    unique = {}
    for item in items:
        unique.setdefault(item["title"].casefold(), item)
    ordered = sorted(
        unique.values(),
        key=lambda item: item["publishedAt"] or "",
        reverse=True,
    )[:30]
    return {
        "source": "Google News RSS",
        "updatedAt": datetime.now(timezone.utc).isoformat(),
        "stories": ordered,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default="news.json")
    args = parser.parse_args()
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(build_feed(), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote headline feed to {output}")


if __name__ == "__main__":
    main()
