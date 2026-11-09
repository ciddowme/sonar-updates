#!/usr/bin/env python3
"""Check the current public mirror README without network access."""

from pathlib import Path
import re
import sys
from urllib.parse import urljoin


if len(sys.argv) > 2:
    raise SystemExit("usage: check_readme.py [README.md]")
path = Path(sys.argv[1]) if len(sys.argv) == 2 else Path("README.md")
text = path.read_text(encoding="utf-8")

if not text.startswith("# Sonarsense"):
    raise SystemExit("README heading must name Sonarsense")
if (
    re.search(r"sonar\s+assistant|сонар\s+ассистент", text, re.IGNORECASE)
    or "SonarSense" in text
):
    raise SystemExit("README contains an old product name")
if re.search(r"\bРФ\b|росси|russia|russian federation", text, re.IGNORECASE):
    raise SystemExit("README contains an unsupported country claim")
links = re.findall(r"\[Releases\]\(([^)]+)\)", text)
if len(links) != 1 or urljoin(
    "https://github.com/ciddowme/sonar-updates/blob/main/README.md", links[0]
) != "https://github.com/ciddowme/sonar-updates/releases":
    raise SystemExit("README Releases link must point to the public mirror")
if not text.endswith("\n") or any(line.endswith((" ", "\t")) for line in text.splitlines()):
    raise SystemExit("README has trailing whitespace or no final newline")

print("README copy check passed")
