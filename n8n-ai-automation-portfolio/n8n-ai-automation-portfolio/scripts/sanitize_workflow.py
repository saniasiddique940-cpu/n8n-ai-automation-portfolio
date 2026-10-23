#!/usr/bin/env python3
"""Sanitize an exported n8n workflow JSON before committing it to GitHub.

Usage: python scripts/sanitize_workflow.py raw/input.json workflows/my-flow/workflow.json
"""
import json
import re
import sys
from pathlib import Path

PATTERNS = [
    (re.compile(r"\bapp[A-Za-z0-9]{14}\b"), "YOUR_BASE_ID"),
    (re.compile(r"\btbl[A-Za-z0-9]{14}\b"), "YOUR_TABLE_ID"),
    (re.compile(r"\bfld[A-Za-z0-9]{14}\b"), "YOUR_FIELD_ID"),
    (re.compile(r"\brec[A-Za-z0-9]{14}\b"), "YOUR_RECORD_ID"),
    (re.compile(r"[\w.+-]+@[\w-]+\.[\w.-]+"), "user@example.com"),
    (re.compile(r"https://[\w-]+\.app\.n8n\.cloud"), "https://YOUR-INSTANCE.app.n8n.cloud"),
    (re.compile(r"\b(?:sk-[A-Za-z0-9_-]{20,}|tvly-[A-Za-z0-9_-]{10,}|gsk_[A-Za-z0-9]{20,}|AIza[A-Za-z0-9_-]{30,})\b"), "REDACTED_KEY"),
]
DROP_TOP_LEVEL = {"pinData", "meta", "versionId", "activeVersionId", "id", "shared", "tags", "staticData"}


def scrub(value):
    if isinstance(value, str):
        for pattern, replacement in PATTERNS:
            value = pattern.sub(replacement, value)
        return value
    if isinstance(value, list):
        return [scrub(v) for v in value]
    if isinstance(value, dict):
        return {k: scrub(v) for k, v in value.items()}
    return value


def main(src: str, dst: str) -> None:
    data = json.loads(Path(src).read_text(encoding="utf-8"))
    for key in DROP_TOP_LEVEL:
        data.pop(key, None)
    data["pinData"] = {}
    data["active"] = False
    for node in data.get("nodes", []):
        node.pop("webhookId", None)
        for cred_type in node.get("credentials", {}):
            node["credentials"][cred_type] = {"id": "REPLACE_ME", "name": "YOUR_CREDENTIAL_NAME"}
    data = scrub(data)
    out = Path(dst)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Sanitized -> {out}")
    print("Next: read the file yourself (prompts, notes, client or personal data), then run scripts/check_exports.py")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    main(sys.argv[1], sys.argv[2])
