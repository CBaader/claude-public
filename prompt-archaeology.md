# Prompt archaeology: what builds up in an instruction file

After eight months of daily use, I audited my agent setup: thirty-odd skill files, three instruction files, a subagent definition and two hooks that inject text. I came away with 98 findings.

Most of the rules still made sense. Prohibitions usually explained their purpose, and operations that needed an exact script had one. The main problem was how much had collected around those rules: notes about the incident that prompted a change, caveats for an old model, numbers copied from an earlier version of the setup.

It was easy to see why someone had written each of these things. It was harder to see why the model still needed to read them on every run.

## What had built up

The most common finding was a rule followed by its history. The instruction was already clear, but a parenthesis explained what it had replaced, when it had changed and what had gone wrong before.

"Learning from the first live run, 25 August." "Before the 25th it skipped every indented line." "Rule history: 30 days until the 22nd, then 21 days, then this."

One skill ended with a 450-word changelog describing five versions of rules already set out in the body. Another devoted a quarter of its length to a disabled method, kept "for reference", along with the dates of the A/B test that had retired it. Keeping that record was understandable. Putting it in the file loaded by the model meant the model had to read two procedures and decide which one applied.

Then there were the numbers. The size of an index appeared in five places, with three different figures. None was current. A list of withheld skills was one name short. A subagent was told that a corpus contained "exactly 12 files", then told two lines later to list the directory. There were 31 files.

Those details are easy to overlook because they sit beside instructions that remain correct. The file gives the model no reliable way to distinguish the stale fact from the valid rule.

Other instructions looked like leftovers from earlier models: capital-letter emphasis without an explanation, a five-by-five scoring grid that repeated two axes already defined above it, fifteen numbered steps for an editing task where the order barely mattered. There were word budgets with a "±15%" tolerance, but no reliable check that the output met them.

Some of that scaffolding may have helped when it was introduced. Its continued presence did not tell me whether it still helped.

The findings I worried about most were broken references. A skill invoked another skill that was no longer available. An instruction named a tool the connector did not expose. A hand-off used a sibling skill's name that had never existed. These can cause an obvious failure, but they can also lead the agent to improvise a substitute. The second outcome is harder to catch because the run can appear to have worked.

## Why it happens

When a run goes wrong, I tend to fix the instruction and record what happened at the same time. The note explains the change to me and to whoever next reads the file. At that point, it is useful.

But the next reader is usually the model. It loads the file again and again, while I rarely return to read the whole thing. The note stays because there is no particular occasion to remove it. Months later, the model is still being told about a bug whose only remaining relevance is the rule that fixed it.

Numbers become stale through much the same process. "The index is about 500 KB" seems like useful context when you have just checked its size. A month later, the index has grown, but nothing in the workflow checks the figure again. If it has been copied into several files, each copy becomes another thing to remember to update.

Model changes are harder to notice. A prompt can continue to produce acceptable results even after some of its instructions have become unnecessary. There is no warning that a scoring grid, a repeated prohibition or a detailed sequence of steps has stopped being needed.

## How I audited it

I started by searching the files the agent actually loads for dates and phrases such as "previously", "changed from", "as of", "retired" and "no longer". I also checked counts, sizes and other numbers that describe the setup.

For each result, I asked what the passage contributes to the next run.

An explanation can be useful. A short reason after a rule helps the model understand when and how to apply it. The full account of the incident that produced the rule usually belongs in version control or a separate changelog.

A number needs more scrutiny. If the agent needs the current value, the instruction should tell it how to obtain that value. If the number has no bearing on the task, I removed it.

I also checked every named skill, tool and file. These references are easy to skim past when editing prose, but they determine whether the instructions can actually be followed.

Before deleting anything, I made a short list of what needed to stay: reasons that help explain a rule, exact scripts for fragile operations, and templates that define a required output. A strict prohibition stays if it guards against a known failure. Brevity alone is a poor reason to remove something useful.

Changes to behaviour need testing. Where I simplified a procedure or removed scaffolding, I ran the skill on the same real input before and after, then compared the results. Removing a redundant history note calls for a lighter check, but I still watched the next run for any unexpected difference.

A model upgrade is a sensible time to repeat the audit, particularly for instructions added to compensate for the previous model's weaknesses.

What surprised me was how little of this looked obviously wrong on its own. Each note had a reason to be there when it was written. Over time, those small additions turned the instruction files into a partial record of maintaining the system. I want to keep that record, but the agent does not need to read all of it to do today's work.
