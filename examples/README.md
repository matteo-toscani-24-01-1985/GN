# Worked planning scenarios for GN (v1.0 beta)

The values below are **hypothetical planning inputs** provided to demonstrate a study-design workflow, not real findings or recommendations for a specific research project. The tool can be run entirely offline from `index.html`. It is important to justify the actual effect size and model assumptions before a real study.

## Scenario A: independent-samples t test

- **Outcome:** systolic blood pressure, measured in mmHg (a quantitative physical measurement).
- **Grouping variable:** two independent treatment-assignment groups, each containing different participants.
- **Scientific target:** a two-sided difference in population means.
- **Illustrative assumptions:** mean difference 6 mmHg; common within-group SD 12 mmHg; Cohen's `d = 6/12 = 0.50`; `α = 0.05`; target power 80%; equal allocation.
- **GN steps:** choose a continuous outcome, two independent groups, the independent-samples t test, `d = 0.5`, 80% power and α = 0.05.
- **Reference check:** under the pooled-variance noncentral-t model, the minimum is **64 completed participants per group**, **128 in total**. This does not account for loss to follow-up.
- **Unequal allocation:** if a 1:2 ratio is entered, GN recalculates the completed sample size with a pooled-variance noncentral-t distribution and separately displays each group count.

## Scenario B: paired t test

- **Outcome:** participant reaction time in milliseconds, observed under two conditions.
- **Design:** each participant completes both conditions; the same individual contributes a paired difference.
- **Scientific target:** a two-sided mean within-person reaction-time difference.
- **Illustrative assumptions:** expected mean paired difference 20 ms, **SD of participant-level paired differences 40 ms**, so `dz = 20/40 = 0.50`; α = 0.05; target power 80%.
- **GN steps:** choose a continuous outcome and two repeated conditions, select paired t test, and use Cohen's `dz = 0.5`.
- **Note:** the relevant SD for `dz` is the *SD of within-person differences*, not the SD of all observations or the two condition SDs separately. Participants are counted once.

## Scenario C: two-factor mixed design

- **Outcome:** systolic blood pressure (mmHg).
- **Between-participants factor:** allocated treatment group (2 levels).
- **Within-participants factor:** measurement occasion (baseline, follow-up 1, follow-up 2).
- **Scientific target:** the **treatment × occasion interaction**, meaning that the time profile differs between groups.
- **Assumptions to document:** specific interaction effect-size definition, common within-cell measurement SD, participant-level correlation `ρ`, sphericity/epsilon assumption, balanced or unequal group allocation and expected completed participants.
- **GN steps:** select *Two-way mixed ANOVA*, choose *interaction*, select *Treatment* and *Time*, then enter the effect size and `ρ`. If unequal group sizes are entered, the resulting factorial estimate is clearly labelled an approximation; seek a design-specific simulation for final high-stakes planning.

## What not to do

A **single five-category agreement rating** is ordinal. Do not change the outcome selector to continuous merely because the answer options are coded 1–5. This beta does not calculate power for ordinal logistic or other ordinal-response analyses. A composite or multi-item scale needs a separate measurement and modelling justification before treating it as a quantitative outcome.
