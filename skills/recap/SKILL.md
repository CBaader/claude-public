---
name: recap
description: Render the session state card — everything done, waiting, parked, and next — in the terminal and to the browser cockpit page. Use when the user says "recap", "where are we", "what's open", or at any staged-skill gate.
effort: low
---

# Recap — Session State Card

Emit the current session state card: the complete open state of the conversation, so the user never needs to scroll back. This file is the **single source of truth** for the card's format and rules; your CLAUDE.md "Session state cards" convention and any staged-skill gates should point here.

## Card format (terminal)

Render as a fenced code block (monospace, visually separated):

```
── STATE ── HH:MM ─────────────────────────────
✅ Done      what changed since the last card (1–3 lines, plain language)
🔶 Waiting   1. ⛔ <decision the user owes — blocking>
             2. ○ <decision — open, can wait>
🅿 Parked    tangents raised mid-flow, handled or queued — never silently dropped
▸ Next       what happens on "continue" (or "nothing pending")
```

## Rules

- **Always-on cadence.** Every turn ends with the card, including clean turns with nothing outstanding (Waiting/Parked render `—`, Next renders "nothing pending"). A pure conversational one-liner (a quick factual answer, a clarification) may skip it only when nothing is open session-wide — no Waiting items, nothing parked, no mid-procedure state; the skip test is the session's open state, never the current turn alone.
- **Complete, not incremental.** Reading only the latest card must suffice — never reference earlier cards or assume scrollback.
- **Stable numbering.** Within a session, a Waiting item keeps its number until resolved; retired numbers are not reused.
- **Blocking vs open.** ⛔ = you cannot proceed without the answer; ○ = decidable later. Mirrors the recap rule in global CLAUDE.md.
- **Plain language.** Name the actual thing (who/what); internal IDs (todo line numbers, action codes) only as trailing parentheticals.
- **Parking lot.** Anything the user raised mid-procedure that is not yet fully closed goes under 🅿 with one clause of status. An empty section is written as `—`, not omitted (the fixed shape is what makes the card scannable).
- `/recap` emits the card and nothing else — no re-analysis, no new work.
- Timestamp: use the current time (run `date +%H:%M` — never from memory).

## Browser cockpit (always, best-effort)

The cockpit page `<your-state-dir>/session-card.html` aggregates the cards of **all** live sessions on this machine — one collapsible section per session, newest update first, with a totals bar ("N sessions · M waiting (X blocking)") and the Mac's name in the header. Sessions not updated today render dimmed; older than 3 days render collapsed (click to expand — display-only, no information is removed). The user opens it once with `open <your-state-dir>/session-card.html` and keeps the tab beside the terminal; it self-refreshes every 30 seconds.

After printing the terminal card, update this session's fragment and rebuild the page:

1. **Write the fragment** to `<your-state-dir>/session-cards/<session-id>.json`, where `<session-id>` is the first 8 hex chars of the session ID visible in the scratchpad directory path (fallback: a slug of the label). Schema:

```json
{
  "label": "Short human topic label",
  "updated": "2026-08-11T10:43:50+0100",
  "done": ["...", "..."],
  "waiting": [{"n": 2, "blocking": true, "text": "..."}],
  "parked": ["..."],
  "next": ["..."]
}
```

- `label`: pick once per session from what the session is about ("Weekly report", "Notes consolidation"); keep it stable for the rest of the session.
- `updated`: from `date +%Y-%m-%dT%H:%M:%S%z` — never from memory (combine with the `date +%H:%M` call for the terminal card timestamp; one command, both formats).
- `waiting` numbering and blocking flags mirror the terminal card exactly (`n` = the stable item number, `blocking` true for ⛔, false for ○). Empty sections are empty arrays.

2. **Rebuild the page**: `python3 build-session-card.py` (shipped next to this SKILL.md; set `CLAUDE_STATE_DIR` to `<your-state-dir>` or edit the `STATE` constant) — reads all fragments, writes the aggregated page. Never edit `session-card.html` directly and never delete another session's fragment; the renderer script is the only writer of the page.

Keep both files out of git (ephemeral, per-machine). A failed write or rebuild never blocks the terminal card — mention it in one clause and move on. Fragment cleanup belongs to your end-of-session skill (delete this session's own fragment and rebuild); abandoned sessions' fragments simply age out visually.
