# Corpus coverage: making an agent read every page of a fixed library

I keep a library of reading notes: around eight hundred short entries in thirty files, each describing one idea, mechanism or test taken from a book, an article or a newsletter. When I read something new, an agent extracts the ideas that might deserve an entry (the candidates) and checks each one against everything already there. This runs as a Claude Code skill, a procedure file the agent follows, and a run means one source, its candidates and all thirty files. The question is "is this covered anywhere?", and it is harder than "where is this covered?". A positive answer needs one good hit. A negative answer is only as good as the breadth of the read.

The usual research pattern for agents is breadth-first: search for the obvious terms, open what looks relevant, follow leads, stop when the answer seems settled. It is the right pattern for finding things. It is the wrong pattern for proving absence. The same idea sits in a library under different words ("compound interest applied to skills" and "compound progress" are one entry), and a search that stops when it is satisfied cannot tell "not found" from "not there".

## Reading everything, slowly

So the first version read everything. Every file, in full, in the main conversation, on every run, before the agent judged a single candidate. It was correct and it was slow. The main session spent most of its window on text that had nothing to do with the candidate at hand, and made its judgement at the end of that window, having read the whole library to find three relevant paragraphs.

I wanted to keep the guarantee and change the delivery.

## Fan out the reading, keep the judgement

The design has four parts.

**A map first.** The library keeps an index: one line per entry with its name, where it lives and a trigger, a short line naming the situation that should bring the idea to mind. The orchestrating session reads the map, not the bodies. That is enough to extract the candidates from the source with some awareness of what the library already holds.

**Readers with assigned files.** The session lists the library's files at run time, never from a stored list, because files get split and merged. It groups them by size into batches small enough for one reader each, with any oversized file taking a reader of its own, and checks before dispatch that every file is assigned to exactly one reader. Then it dispatches all the readers in a single message so they run concurrently. Each reader is told the candidates, given its files, and told to read them in full.

**Digests, not summaries.** A reader does not summarise its files. For each candidate, it returns the entries in its files that bear on it: the entry name and location, a grade (covers: the same mechanism is already written down; partial overlap: part of it is; adjacent: same territory, different move), one or two sentences quoted verbatim, and a line on how it relates or differs. It is told to err toward inclusion, because under-reporting is the failure mode: the orchestrator can discard an adjacent entry cheaply but cannot recover one that was never reported. A "covers" grade is a signal, not a verdict. And each reader reports how many entries it saw in each file.

That last line is the integrity check. A reader that hit a tool limit, or skimmed, or opened the wrong file, reports an entry count that does not match the file. The orchestrator compares the counts to the files and knows which reads to distrust.

**The orchestrator re-reads the finalists.** No candidate gets a verdict off a digest alone. For each one, the session takes the two or three strongest reported entries, reads their actual text from the files, and compares mechanism rather than topic. Where the reported entries span several files, it reads them together, because a candidate can duplicate a combination of entries while matching none of them by name. One candidate rated new after a full run turned out, on that cross-file re-read, to be three existing entries under one title. Then the session presents its recommendations, and I make the call.

## Five things that must not break

Writing the design in June 2026, I listed what the faster version had to preserve, and the list has not changed since:

1. Every file is read in full, by a reader or, if a reader fails, by the orchestrator itself.
2. Before any "already covered" verdict, the orchestrator re-reads the actual entry text.
3. Candidates are presented for a decision, never added automatically.
4. When in doubt, draft it: a possible miss appears as a draft for me to reject, not as a silent skip.
5. Re-read the section an approved entry is going into immediately before writing it, because another session may have changed it.

Everything else is tunable: the reader model, the grouping of files, the shape of the digest. These five are what "without skipping any" means.

## What went wrong, and what fixed it

**Readers that finish without reporting.** On one run, two readers read their files and went idle without sending their digests back. The results sat in their own transcripts. The fix was a sentence at the end of every reader prompt: deliver your digest as your final action; do not go idle without sending it. If one still goes quiet, the orchestrator sends one nudge, then re-dispatches.

**Dropped readers.** After the fan-out, the orchestrator confirms a digest came back for every assigned file and that each entry count is plausible. A missing, empty or implausible file gets its reader re-dispatched once. If that fails too, the orchestrator reads the file itself. It never finalises with a file uncovered. This is the dull part of the design and the part that makes the guarantee real.

**Switching without proof.** I did not retire the read-everything version on the day the fan-out was written. For the first few runs on real sources, not test inputs, both paths ran on the same input and I compared the verdicts: did the parallel path flag every overlap the full read flagged? It did, across four or five runs, and only then did the old path come out of the skill. If it had missed one, the fix would have been richer digests or smaller batches, not a lower bar.

**The map outgrew the window.** By August, two months in, the index itself had grown past what the orchestrator could read in one go, and a run degraded into improvised searches. The fix was a derived compact map, names and locations only, regenerated by a script and never edited by hand. The full index is now read by its own readers, in chunks. Those index readers were later moved to the end of the run, after something has been approved and needs placing, which means deciding where it sits in the index and which entries it links to. Before that, they took about a third of a run's tokens and were wasted whenever every candidate was skipped.

**Reader cost.** Readers started on the largest model, Opus, on the principle that tokens were the cheap resource. At about three million tokens a run they were not. A side-by-side test on two pairs of files and nine candidates found that Sonnet as reader reported every entry the large model had graded as partial overlap, saw the same entry counts, and missed about a quarter of the weak adjacent links. No verdict would have changed. Readers now run on Sonnet, judgement stays on Opus, and the finalist re-read makes up for the thinner adjacency.

## When to use this

Most questions an agent asks of a corpus are find-shaped, and the breadth-first pattern serves them well. This design is for the other kind: the question whose honest answer may be "no, nowhere", where a confident wrong "no" costs more than the read. Duplicate checks, completeness audits, "has this rule already been written down somewhere", "does any contract in this folder contain this clause". For those, the mechanism has to be able to show that it read everything: an assignment that covers the listing, a count per file, a fallback when a reader drops, and a judge who reads the originals before ruling.
