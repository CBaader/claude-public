#!/usr/bin/env python3
"""UserPromptSubmit hook: point-of-action reminder to verify checkable facts.

When a prompt looks like it is asking for a live, checkable fact (time, date,
price, file contents, library/API detail), inject a short reminder so the
"never from memory" rule fires at the moment of action rather than relying on
a session-start instruction file surviving in context.

Design notes:
- Lean generous on triggers: a false positive costs one injected line; a false
  negative is the fabricated-fact failure this exists to prevent.
- Never block or error the prompt. Any parse failure exits 0 silently.
"""
import json
import re
import sys

# Trigger phrases per category. Generous by design.
PATTERNS = [
    # time
    r"\bwhat(?:'?s| is)?\s+the\s+time\b", r"\bwhat\s+time\b", r"\bcurrent\s+time\b",
    r"\bo'?clock\b", r"\btime\s+is\s+it\b", r"\btime\s+now\b",
    # date / day / year
    r"\bwhat(?:'?s| is)?\s+(?:the\s+)?date\b", r"\bwhat\s+day\b", r"\btoday'?s?\s+date\b",
    r"\bwhat\s+year\b", r"\bcurrent\s+date\b", r"\bwhat\s+month\b",
    # price / cost
    r"\bhow\s+much\s+(?:is|does|are|would|will)\b", r"\bwhat(?:'?s| is)?\s+the\s+(?:price|cost)\b",
    r"\bcost\s+of\b", r"\bprice\s+of\b", r"[$£€]\s?\d",
    # file contents
    r"\bwhat'?s?\s+in\s+(?:the\s+|my\s+|this\s+)?(?:file|\S+\.\w+)", r"\bcontents?\s+of\b",
    r"\bwhat\s+does\s+(?:the\s+)?\S+\s+(?:say|contain)\b",
    # library / API / version
    r"\b(?:latest|current|newest)\s+version\b", r"\bwhat\s+version\b", r"\bwhich\s+version\b",
    r"\bapi\s+(?:for|of|endpoint)\b", r"\bdoes\s+\S+\s+support\b",
]
_RX = [re.compile(p, re.IGNORECASE) for p in PATTERNS]

REMINDER = (
    "[verify-facts hook] This prompt may be asking for a live, checkable fact "
    "(time / date / price / file contents / library or API detail). Do NOT answer "
    "from memory. Run the tool in this same message first "
    "- `date` for the time, read the file, the CLI, the relevant doc - or say plainly "
    "that you have not checked. No exceptions."
)


def main() -> int:
    try:
        data = json.load(sys.stdin)
    except Exception:
        return 0
    prompt = data.get("prompt", "")
    if not isinstance(prompt, str) or not prompt.strip():
        return 0
    if not any(rx.search(prompt) for rx in _RX):
        return 0
    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "UserPromptSubmit",
            "additionalContext": REMINDER,
        }
    }))
    return 0


if __name__ == "__main__":
    sys.exit(main())
