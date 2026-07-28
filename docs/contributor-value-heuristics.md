# Contributor Value Heuristics

## Purpose

This note defines a future direction for the Contributor and Vendor Value
reviewer. Its purpose is to identify the people responsible for most of a
project's **evidence-supported delivered value**, including implementation,
testing, debugging, review, documentation, and operational enablement.

It is not an employee-performance rating, compensation assessment, contractual
acceptance decision, or statement of hours worked. It must not infer any of
those from repository activity.

## Conclusion

PR count, commit count, lines added, lines deleted, and code churn are useful
discovery signals, but they are poor measures of value. They measure activity
or the volume of change, and can reward PR splitting, verbosity, generated
code, or rework. They can also undervalue deletion, simplification, review,
testing, debugging, documentation, and operational work.

The useful unit is a **feature or meaningful change**, not a Git commit and not
a person. First assess the feature's delivered value and task magnitude from
evidence. Then attribute the documented shares of that work to contributors.

This follows research on development value, which distinguishes the amount of
code from its structural importance and impact. A change to a critical workflow
or integration can be more valuable than a much larger auxiliary change.
[Yin, *Quantifying the Development Value of Code Contributions* (2018)](https://www2.eecs.berkeley.edu/Pubs/TechRpts/2018/EECS-2018-174.pdf).

## What To Assess

Create a feature/change unit by grouping the linked PRs, commits, issue,
documentation, and follow-up fixes that deliver one coherent result. Do not
merge unrelated work merely because it has the same author.

For each unit, record the following separately.

| Dimension | Question | Typical evidence |
|---|---|---|
| Outcome value | What customer, commercial, operational, risk-reduction, or maintainability outcome did it deliver? | PR/issue purpose, product documentation, release notes, operating evidence |
| Task magnitude | How substantial was the work to deliver safely? | Requirements, acceptance criteria, affected workflows, integration/data/security boundaries, dependencies, test/debug and review work |
| Delivery quality | Was the result made durable and safe to change or operate? | Tests, review discussion and resolution, defect follow-ups, documentation, rollout/rollback evidence |
| Contribution share | Who materially implemented, tested, debugged, reviewed, designed, documented, or operationalized it? | PR authorship, commits, reviews, linked issues, credited documentation or runbooks |
| Confidence | How complete and reliable is the evidence? | Exact locators, source access limits, unresolved attribution or outcome gaps |

Task magnitude must be an evidence-backed band, not inferred from changed-line
count. Useful indicators include the number and importance of affected
boundaries, cross-system dependencies, migrations, security or data handling,
unknowns discovered during debugging, and the breadth of required tests. The
best available research on Agile estimation likewise finds functional
requirements, user stories, definition of done, UI wireframes, acceptance
criteria, and dependencies more useful than a code diff alone.
[Alenezi et al., *Towards Just-Enough Documentation for Agile Effort Estimation* (2021)](https://arxiv.org/abs/2107.02420).

## How To Use Repository Metrics

Use repository metrics to find and corroborate work; do not use them as the
value score.

| Signal | Legitimate use | Not a valid conclusion |
|---|---|---|
| PR count | Find candidate work and collaboration boundaries | More PRs means more value |
| Lines added/deleted or churn | Check scope and identify large refactors or generated code | More changed lines means more effort or value |
| Commit count | Locate history and follow-up fixes | More commits means more work or ownership |
| Review activity | Identify collaboration and possible quality contribution | Comment count proves review quality |
| Time to merge | Identify a possible dependency or review burden | Longer duration proves task difficulty |

Individual PR-level effort prediction is an active but distinct field: it can
help plan and track a work item, but it does not establish the business value
of that work item. [Maddila, Bansal, and Nagappan, *Predicting Pull Request
Completion Time* (ESEC/FSE 2019)](https://www.microsoft.com/en-us/research/publication/predicting-pull-request-completion-time-a-case-study-on-large-scale-cloud-services/).

## Attribution And Ranking

Attribute credit to the people with evidenced material contributions to a
feature/change unit. The primary author is not automatically the sole creator
of value: a contributor may materially test, debug, review, design, document,
or make the feature operable. Conversely, an account that merely merged or
commented on work receives no inferred credit.

Present outcome value, task magnitude, delivery quality, contribution share,
and confidence as separate fields. Do not collapse them into a deceptively
precise universal productivity score. For a within-audit 80-percent ranking,
use WGO's published coarse bands—`critical = 8`, `high = 5`,
`meaningful = 3`, `bounded = 2`, and `minor = 1`—selected from the evidenced
outcome and task magnitude. They are an ordering aid only; retain the source
links and confidence behind every aggregate.

For the requested 80-percent list, include the smallest set of contributors
whose attributed feature-value units account for approximately 80% of the
evidence-supported total. This is not the top 80% of accounts. Show the
remaining long tail as an aggregate count and value share unless its individual
entries are decision-relevant.

Where a project spans more than 12 months, produce:

1. one list from the project start through the audit cutoff; and
2. one list for each consecutive, non-overlapping 12-month period counted
   backwards from the audit cutoff.

Do not mix periods or assign credit across a period boundary without stating
the reason. A feature that spans periods should retain its evidence links and
be apportioned only when the dated evidence supports it; otherwise mark the
period allocation as uncertain.

## Limits And Safeguards

Effort and value are not person-independent. A controlled study found material
variation in the effort different developers spent on the same tasks, including
when using relative estimates. [Jørgensen and Escott, *Relative Estimates of
Software Development Effort* (2021)](https://www.sciencedirect.com/science/article/abs/pii/S0950584921002251).

Consequently, WGO must:

- use an explicit audit cutoff and evidence links;
- label inaccessible PR, issue, review, documentation, or runtime evidence as a
  limitation;
- keep value, task magnitude, contribution share, and confidence separate;
- never substitute LoC, commit volume, or account control for missing feature
  evidence; and
- state when a result is unsuitable for an employment, compensation, or
  contractual decision.

This multi-dimensional approach is consistent with the SPACE framework, which
argues that developer productivity cannot be represented by a single activity
metric. [Forsgren et al., *The SPACE of Developer Productivity* (2021)](https://www.microsoft.com/en-us/research/publication/the-space-of-developer-productivity-theres-more-to-it-than-you-think/).

## References

- H. Yin. [*Quantifying the Development Value of Code Contributions* (2018)](https://www2.eecs.berkeley.edu/Pubs/TechRpts/2018/EECS-2018-174.pdf).
- S. Alenezi et al. [*Towards Just-Enough Documentation for Agile Effort Estimation* (2021)](https://arxiv.org/abs/2107.02420).
- C. Maddila, C. Bansal, and N. Nagappan. [*Predicting Pull Request Completion Time* (ESEC/FSE 2019)](https://www.microsoft.com/en-us/research/publication/predicting-pull-request-completion-time-a-case-study-on-large-scale-cloud-services/).
- M. Jørgensen and E. Escott. [*Relative Estimates of Software Development Effort* (2021)](https://www.sciencedirect.com/science/article/abs/pii/S0950584921002251).
- N. Forsgren et al. [*The SPACE of Developer Productivity* (2021)](https://www.microsoft.com/en-us/research/publication/the-space-of-developer-productivity-theres-more-to-it-than-you-think/).
