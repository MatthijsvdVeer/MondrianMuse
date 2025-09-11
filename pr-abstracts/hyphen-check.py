import argparse
import os
import subprocess
import sys
from typing import Dict, List, Tuple

# Mapping of offender names to their Unicode characters
OFFENDERS: Dict[str, str] = {
    "en-dash": "\u2013",            # – U+2013
    "em-dash": "\u2014",            # — U+2014
    "non-breaking hyphen": "\u2011", # ‑ U+2011
}


def detect_offenders(text: str) -> List[Tuple[str, str, str]]:
    """
    Return a list of tuples: (name, char, codepoint) for each offender found at least once.
    """
    found: List[Tuple[str, str, str]] = []
    for name, ch in OFFENDERS.items():
        if ch in text:
            codepoint = f"U+{ord(ch):04X}"
            found.append((name, ch, codepoint))
    return found


message_header = "You hyphened too deep, and too greedily"


def format_comment(found: List[Tuple[str, str, str]]) -> str:
    lines = [message_header, "", "Offenders:"]
    for name, ch, code in found:
        # Include both the friendly name, the glyph, and its Unicode code point
        lines.append(f"- {name} ({ch}) {code}")
    return "\n".join(lines)


def comment_on_pr(pr_id: str, body: str) -> None:
    try:
        subprocess.run(["gh", "pr", "comment", pr_id, "--body", body], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Failed to post PR comment: {e}", file=sys.stderr)


def main() -> int:
    ap = argparse.ArgumentParser(description="Detect en/em dashes and non-breaking hyphens in abstract and comment on PR when present.")
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

    found = detect_offenders(text)

    if found:
        body = format_comment(found)
        # Print for logs (preserve non-ASCII)
        print(body)
        pr_id = args.pr_id or os.environ.get("PR_ID")
        if pr_id:
            comment_on_pr(pr_id, body)
        # Non-zero to allow gating; caller can `|| true` if they don't want failures
        return 1

    # No offenders: do not comment anything, succeed silently
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

