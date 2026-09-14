#!/usr/bin/env python3
"""Rebuild the multi-session cockpit page state/session-card.html.

Reads every fragment in state/session-cards/*.json (one per Claude session,
written by /recap) and renders one aggregated page: totals bar, one section
per session sorted newest-update-first. Age display, day-based dimming and
3-day collapsing are computed client-side so they stay current on the page's
30s self-refresh even when no session has written for hours.

Fragment schema (all keys optional except label):
  {
    "label":   "Weekly report",
    "updated": "2026-08-11T10:21:00+0100",   # falls back to file mtime
    "done":    ["...", ...],
    "waiting": [{"n": 2, "blocking": true, "text": "..."}, ...],
    "parked":  ["...", ...],
    "next":    ["...", ...]
  }

Stdlib only. Never deletes fragments — cleanup belongs to your end-of-session skill.

State directory: $CLAUDE_STATE_DIR if set, else ~/.claude/state.
"""

import html
import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

STATE = Path(os.environ.get("CLAUDE_STATE_DIR", Path.home() / ".claude" / "state"))
FRAG_DIR = STATE / "session-cards"
OUT = STATE / "session-card.html"


def machine_name() -> str:
    try:
        return subprocess.run(
            ["scutil", "--get", "ComputerName"],
            capture_output=True, text=True, timeout=5,
        ).stdout.strip() or "this Mac"
    except Exception:
        import platform
        return platform.node() or "this Mac"


def parse_updated(raw, fallback: float) -> datetime:
    if isinstance(raw, str):
        for fmt in ("%Y-%m-%dT%H:%M:%S%z", "%Y-%m-%dT%H:%M%z"):
            try:
                return datetime.strptime(raw, fmt)
            except ValueError:
                pass
        try:
            return datetime.fromisoformat(raw)
        except ValueError:
            pass
    return datetime.fromtimestamp(fallback).astimezone()


def load_fragments():
    frags, bad = [], []
    if FRAG_DIR.is_dir():
        for p in sorted(FRAG_DIR.glob("*.json")):
            try:
                data = json.loads(p.read_text())
                data["_updated"] = parse_updated(
                    data.get("updated"), p.stat().st_mtime)
                data.setdefault("label", p.stem)
                frags.append(data)
            except (json.JSONDecodeError, OSError):
                bad.append(p.name)
    frags.sort(key=lambda f: f["_updated"], reverse=True)
    return frags, bad


def esc(s) -> str:
    return html.escape(str(s))


def render_list(items, li_class="") -> str:
    cls = f' class="{li_class}"' if li_class else ""
    if not items:
        return '<li class="empty">—</li>'
    return "".join(f"<li{cls}>{esc(i)}</li>" for i in items)


def render_waiting(items) -> str:
    if not items:
        return '<li class="empty">—</li>'
    out = []
    for w in items:
        cls = "blocking" if w.get("blocking") else "open"
        num = f'{w["n"]}. ' if w.get("n") is not None else ""
        out.append(f'<li class="{cls}">{num}{esc(w.get("text", ""))}</li>')
    return "".join(out)


def render_section(f) -> str:
    iso = f["_updated"].isoformat()
    hhmm = f["_updated"].strftime("%H:%M")
    return f"""<details class="card" data-updated="{iso}" open>
<summary><span class="label">{esc(f["label"])}</span>
<span class="meta">updated {hhmm} <span class="age"></span></span></summary>
<section class="done"><h2>✅ Done</h2><ul>{render_list(f.get("done"))}</ul></section>
<section class="waiting"><h2>🔶 Waiting on you</h2><ul>{render_waiting(f.get("waiting"))}</ul></section>
<section class="parked"><h2>🅿 Parked</h2><ul>{render_list(f.get("parked"))}</ul></section>
<section class="next"><h2>▸ Next</h2><ul>{render_list(f.get("next"))}</ul></section>
</details>"""


def main() -> int:
    frags, bad = load_fragments()
    n_wait = sum(len(f.get("waiting") or []) for f in frags)
    n_block = sum(
        1 for f in frags for w in (f.get("waiting") or []) if w.get("blocking"))
    totals = (f'{len(frags)} session{"s" if len(frags) != 1 else ""}'
              f' · {n_wait} waiting ({n_block} blocking)')
    now = datetime.now().astimezone()
    sections = "\n".join(render_section(f) for f in frags) or \
        '<p class="empty">No session fragments found.</p>'
    warn = (f'<p class="warn">Unreadable fragments skipped: {esc(", ".join(bad))}</p>'
            if bad else "")

    page = f"""<!doctype html>
<html><head><meta charset="utf-8">
<meta http-equiv="refresh" content="30">
<title>Sessions — {esc(machine_name())}</title>
<style>
body {{ font-family: -apple-system, "Helvetica Neue", Arial, sans-serif; margin: 0; background: #f5f5f2; color: #111; }}
.wrap {{ max-width: 680px; margin: 24px auto; padding: 0 16px; }}
h1 {{ font-size: 16px; color: #666; font-weight: 600; letter-spacing: .04em; }}
h1 .t {{ float: right; color: #999; font-weight: 400; }}
.totals {{ background: #1565c0; color: #fff; border-radius: 8px; padding: 10px 16px; font-size: 15px; font-weight: 600; margin-bottom: 16px; }}
details.card {{ background: #fff; border: 1px solid #ddd; border-radius: 8px; margin-bottom: 14px; padding: 0 16px 4px; }}
details.card summary {{ cursor: pointer; padding: 12px 0; font-size: 15px; list-style: none; }}
details.card summary::-webkit-details-marker {{ display: none; }}
details.card summary .label {{ font-weight: 600; }}
details.card summary .meta {{ float: right; color: #999; font-size: 13px; }}
details.card.dim {{ opacity: .55; }}
section {{ border-top: 1px solid #eee; padding: 8px 0; }}
section h2 {{ margin: 0 0 4px; font-size: 12px; letter-spacing: .05em; text-transform: uppercase; }}
.done h2 {{ color: #2e7d32; }} .waiting h2 {{ color: #e65100; }} .parked h2 {{ color: #555; }} .next h2 {{ color: #1565c0; }}
ul {{ margin: 0; padding-left: 20px; font-size: 14px; line-height: 1.5; }}
.waiting li.blocking::marker {{ content: "⛔ "; }} .waiting li.open::marker {{ content: "○ "; }}
.empty {{ color: #aaa; font-style: italic; }}
.warn {{ color: #b71c1c; font-size: 13px; }}
</style></head>
<body><div class="wrap">
<h1>SESSIONS — {esc(machine_name()).upper()} <span class="t">rebuilt {now.strftime("%H:%M")}</span></h1>
<div class="totals">{totals}</div>
{sections}
{warn}
<script>
const now = new Date();
document.querySelectorAll("details.card").forEach(d => {{
  const t = new Date(d.dataset.updated);
  const mins = Math.round((now - t) / 60000);
  const age = mins < 60 ? mins + "m ago"
            : mins < 2880 ? Math.round(mins / 60) + "h ago"
            : Math.round(mins / 1440) + "d ago";
  d.querySelector(".age").textContent = "· " + age;
  const sameDay = t.toDateString() === now.toDateString();
  if (!sameDay) d.classList.add("dim");
  if (now - t > 3 * 86400000) d.removeAttribute("open");
}});
</script>
</div></body></html>
"""
    OUT.write_text(page)
    print(f"session-card.html rebuilt: {totals}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
