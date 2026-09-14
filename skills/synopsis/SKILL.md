---
name: synopsis
description: Distil an article, email, or long-form content into a plain-language synopsis.
argument-hint: "[URL, email reference, or paste content]"
effort: medium
---

# Synopsis

Distil an article, email, or any long-form content into a plain-language synopsis.

## Input

The user provides content via one of:
- Pasted text (article body, email content)
- A URL (fetch via WebFetch)
- An email or message pasted in
- A file path (read from disk)

If the user passed an argument, use it to identify the content source. If the content is a teaser or summary linking to a full article, fetch the full article.

**Verify completeness before synopsising.** Fetched web content is often partial — paywalls, cookie walls, "subscribe to continue" stubs, pages that cut off mid-article. Check for an abrupt ending, subscription prompts, or a length implausibly short for the piece. If the text is (or may be) incomplete, say so prominently at the top of the synopsis and cover only what was actually retrieved — or ask the user to paste the full text. Never present a synopsis of a fragment as a complete read: the synopsis replaces the original, so a silent gap is invisible to the user.

## Output

For each distinct idea or section in the content:

- **Plain-language synopsis**: Explain as if to a non-expert. No jargon, no economics language, no academic framing. Use concrete analogies. The user hasn't read the content - this IS their read.
- **So what?**: One sentence on why this matters or what action it implies. Skip if the content is purely informational.

## Length

The synopsis is a **replacement document**, not a gateway. The user is not going to read the original — the synopsis IS their read. That justifies a higher word count than a typical abstract or executive summary. Anchor on the empirical NLP-research band of 15–30% compression (best comprehension preservation per ACL/Stanford work), pushed slightly higher at shorter lengths where structure preservation matters more.

| Original length | Synopsis target | Notes |
|----------------|----------------|-------|
| < 500 words | ~60% (min 150 words) | Short pieces need full structure |
| 500-1,500 words | ~40% | Cover every section with "so what" per section |
| 1,500-4,000 words | ~30% | Every section gets at least a sentence; key ones get a paragraph |
| 4,000-8,000 words | ~22% | Detailed treatment; diminishing returns starting |
| 8,000-15,000 words | ~17% | Cover every TOC item, even minor ones |
| 15,000+ words | ~12-15% | No hard ceiling - cover every section |

Minimum 150 words. No maximum. The percentages are targets, not constraints — use as many words as the content warrants; near a band boundary, interpolate between the adjacent percentages rather than jumping. Erring long is preferred to erring short: a section dropped from a synopsis is a section the user never sees.

## Style rules

- Actionable essence in clear prose — be detailed but not verbose
- Frontload "so what?" per section, not just at the top
- Cover every section of the original, even if some get only a sentence
- Verbatim quotes only when a single sentence carries the argument unmistakably; otherwise paraphrase
- No structured tables for narrative content (tables are a triage shortcut, not a replacement read)
- British English
- Flowing paragraphs, bullet points only when they genuinely aid clarity
- State conclusion or action first, then supporting detail
- Do not append meta-commentary about word counts, percentages, or "within target band" — the user can see the length

## What this skill does NOT do

- No comparison against a knowledge base (a separate skill's job)
- No quality-bar assessment or re-read test
- No email management (delete, archive, label)
- No commit or file writing unless explicitly asked
