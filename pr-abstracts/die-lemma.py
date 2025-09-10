import argparse
import json
import os
import subprocess
import sys
from typing import List, Set

import spacy

# Ensure spaCy model is available
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    try:
        from spacy.cli import download
        download("en_core_web_sm")
        nlp = spacy.load("en_core_web_sm")
    except Exception as e:
        print(f"Failed to load/download spaCy model: {e}", file=sys.stderr)
        sys.exit(2)

# Offenders to detect by lemma (case-insensitive)
OFFENDERS = [
    "delve",
    "equip",
    "empower",
    "navigate",
    "landscape",
    "enhance",
    "insight",
]

def extract_lemmas(text: str) -> Set[str]:
    doc = nlp(text)
    # Alpha-only tokens for clarity; map to lowercase lemmas
    return {t.lemma_.lower() for t in doc if t.is_alpha}

def find_offenders(lemmas: Set[str]) -> List[str]:
    found = sorted({w for w in OFFENDERS if w.lower() in lemmas})
    # Return original-cased words for display (capitalize first letter)
    return [w.capitalize() for w in found]

def comment_on_pr(pr_id: str, body: str) -> None:
    # Use gh CLI to comment, relying on GH_TOKEN already present in env
    try:
        subprocess.run(["gh", "pr", "comment", pr_id, "--body", body], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Failed to post PR comment: {e}", file=sys.stderr)

def main() -> int:
    ap = argparse.ArgumentParser(description="Detect discouraged lemmas in abstract and optionally comment on PR")
    ap.add_argument("--file", help="Path to abstract file to scan")
    ap.add_argument("--abstract", help="Abstract text to scan (alternative to --file)")
    ap.add_argument("--pr-id", help="PR number/id to comment on when offenders are found")
    args = ap.parse_args()

    if not args.file and not args.abstract:
        print("No input provided. Use --file or --abstract", file=sys.stderr)
        return 2

    if args.file:
        try:
            with open(args.file, "r", encoding="utf-8") as f:
                text = f.read()
        except Exception as e:
            print(f"Failed to read file '{args.file}': {e}", file=sys.stderr)
            return 2
    else:
        text = args.abstract or ""

    lemmas = extract_lemmas(text)
    offenders = find_offenders(lemmas)

    if offenders:
        # Output list of offenders (JSON array for easy machine parsing)
        print(json.dumps(offenders, ensure_ascii=False))
        # Comment on the PR if PR id provided
        pr_id = args.pr_id or os.environ.get("PR_ID")
        if pr_id:
            body = (
                "🚫 Detected discouraged words (by lemma) in the abstract: "
                + ", ".join(offenders)
                + "\nPlease consider rephrasing."
            )
            comment_on_pr(pr_id, body)
        return 1  # non-zero can help workflows gate follow-up steps if desired
    else:
        msg = "No violations found"
        print(msg)
        return 0


if __name__ == "__main__":
    raise SystemExit(main())
