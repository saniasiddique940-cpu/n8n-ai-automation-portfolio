#!/usr/bin/env python3
"""Validate every workflow JSON under workflows/: structure, connections, and leaked secrets.

Exit code 1 if anything looks wrong (used by CI and safe to run before each commit).
"""
import json
import re
import sys
from pathlib import Path

SECRET_PATTERNS = {
    "Anthropic/OpenAI-style key": re.compile(r"\bsk-[A-Za-z0-9_-]{20,}"),
    "Tavily key": re.compile(r"\btvly-[A-Za-z0-9_-]{10,}"),
    "Groq key": re.compile(r"\bgsk_[A-Za-z0-9]{20,}"),
    "Google API key": re.compile(r"\bAIza[A-Za-z0-9_-]{30,}"),
    "GitHub token": re.compile(r"\bgh[pousr]_[A-Za-z0-9]{30,}"),
    "Bearer token": re.compile(r"Bearer\s+[A-Za-z0-9._-]{20,}"),
    "Airtable id": re.compile(r"\b(?:app|tbl|fld|rec)[A-Za-z0-9]{14}\b"),
    "n8n cloud URL": re.compile(r"https://(?!YOUR-INSTANCE)[\w-]+\.app\.n8n\.cloud"),
    "email address": re.compile(r"[\w.+-]+@(?!example\.com)[\w-]+\.[\w.-]+"),
}


def check(path: Path) -> list[str]:
    problems = []
    raw = path.read_text(encoding="utf-8")
    try:
        data = json.loads(raw)
    except json.JSONDecodeError as exc:
        return [f"invalid JSON: {exc}"]
    nodes = data.get("nodes")
    if not isinstance(nodes, list) or not nodes:
        return ["no nodes"]
    names = [n.get("name") for n in nodes]
    if len(names) != len(set(names)):
        problems.append("duplicate node names")
    for src, kinds in data.get("connections", {}).items():
        if src not in names:
            problems.append(f"connection from unknown node '{src}'")
        for branches in kinds.values():
            for branch in branches:
                for target in branch:
                    if target["node"] not in names:
                        problems.append(f"connection to unknown node '{target['node']}'")
    for node in nodes:
        for cred in node.get("credentials", {}).values():
            if cred.get("id") != "REPLACE_ME":
                problems.append(f"node '{node['name']}' has a real credential id")
        if node.get("type") == "n8n-nodes-base.webhook" and node["parameters"].get("authentication", "none") == "none":
            problems.append(f"webhook '{node['name']}' has no authentication")
    for label, pattern in SECRET_PATTERNS.items():
        if pattern.search(raw):
            problems.append(f"possible leak: {label}")
    return problems


def main() -> int:
    files = sorted(Path("workflows").rglob("*.json"))
    if not files:
        print("No workflow files found under workflows/")
        return 1
    failed = False
    for f in files:
        issues = check(f)
        print(("FAIL " if issues else "ok   ") + str(f))
        for issue in issues:
            print("   - " + issue)
        failed = failed or bool(issues)
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
