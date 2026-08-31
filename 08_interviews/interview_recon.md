# Interview Reconnaissance Protocol

Evergreen drills build transferable skill. Reconnaissance checks that those drills
still resemble what current employers publicly say they evaluate. It calibrates
preparation; it does not replace systematic learning or create a company-question
archive.

## When to run it

Run one short reconnaissance session:

1. when serious applications begin for a role family;
2. before an actual interview loop, prioritizing that company and role; and
3. optionally every 4–6 weeks during an active search when target roles change.

This is deliberately **not** a weekly 26-week assignment. Copy
[the template](interview_recon.template.md) for each session and date every source
or report when the date is available.

## Ethical and evidence rules

Use only material that is intentionally public. Do not seek or preserve leaked
assessments, confidential question banks, stolen/private materials, or content a
candidate was prohibited from sharing. Paraphrase representative practice
questions rather than copying reported prompts verbatim.

Prefer sources in this order:

1. official company interview-preparation pages;
2. official engineering, recruiting, conference, or technical talks;
3. recent public candidate reports on established interview/job sites;
4. recent Reddit or community reports, explicitly labeled anecdotal; and
5. general interview-preparation sites for extra practice examples only.

Interview loops change. Record the research date, the source date when known, and
whether a claim is official, corroborated, or anecdotal. One report is a lead, not
a fact about every team.

## Role families to sample

Choose only the families relevant to the active search: early-career/general SWE,
C++ or systems SWE, embedded-adjacent and hardware/software integration, robotics
SWE, perception/CV, CUDA/GPU, edge inference, or factory automation and machine
interfaces. For a real application, the exact company and job description take
priority over the generic family.

## Questions to ask of the evidence

- Which concepts recur across independent sources?
- What must be coded without reference material, and at what implementation depth?
- How much C++ ownership/lifetime knowledge, OS/concurrency/networking, debugging,
  and system design appears?
- For perception roles, how much metrics, tracking, coordinate-frame, and camera
  geometry reasoning appears?
- For GPU roles, how much CUDA indexing, memory, synchronization, profiling, and
  performance-evidence reasoning appears?
- Which parts of your own artifacts are likely to be probed?
- Which topic appears repeatedly across relevant roles, and which appeared only
  once?

## Convert findings into practice

Map each recurring competency to an existing lab, gate, or interview drill. For a
real gap, write a fresh equivalent exercise: change the domain, data, constraints,
and edge cases so the task tests transfer rather than recognition. For example,
turn a producer/consumer theme into a new bounded-worker problem, coalescing into a
new lane/address table, or IoU/tracking into a new numerical sequence.

Do **not** change the permanent curriculum because one employer reportedly asks an
unusual question. Keep narrow gaps in company-specific preparation. Consider a
core change only after repeated evidence across several relevant roles exposes a
genuine foundation missing from the course.

The output is one short dated note containing sources, stages, recurring
competencies, 5–15 paraphrased public practice questions, curriculum coverage,
rehearsal actions, and topics deliberately left outside the core.
