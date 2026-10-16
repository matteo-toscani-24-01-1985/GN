# GN v1.0 beta — Statistical methods and implementation notes

This technical companion describes what the app **currently calculates**, not a general derivation of all possible power analyses. Computations are prospective, conditioned on a chosen *true* effect size, nominal type-I error rate α, specified sampling design, and target power. The result is the smallest sample found within the app's integer search grid; it does not account for all real-world uncertainties.

## 1. Conventions, sample counts, and critical values

Let `B` = number of **independent between-subject cells** (Cartesian product of the between-person factor levels), `M` = number of repeated conditions on each person, `n_b` = planned completed sample in independent cell `b`, and `N = Σ_b n_b` = distinct participants. Let `Q` be number of numerical covariates. Repeated observations **never multiply `N`**.

- For equal groups, `n_b = n` and `N = Bn`. For **unequal groups**, users supply positive relative weights `w_b`. The engine sets `n_b(n) = ceil(n × w_b / min(w))`; it searches integer `n` and displays resulting per-cell counts. The suggested sample is minimal *on this ratio-constrained grid*, not necessarily the globally minimum sample across all possible integer allocations. Slight deviations from the exact input ratio can result from rounding.
- It computes critical thresholds for a one- or two-sided t test, or upper-tail F, according to α, and evaluates the noncentral distribution under the specified alternative.
- Search is by progressively increasing and then bisecting feasible integer values, capped at approximately 250,000 distinct participants. Monotonic power is assumed within the searched design family; this is not a general optimizer over statistical designs.
- Optional expected attrition `a` produces `ceil(n_b / (1-a))` recruits for each independent cell. Attrition does not modify power for the completed sample.

## 2. One-sample and paired t tests

For Cohen's `d = |μ − μ₀|/σ` (one-sample) or `d_z = |μ_D|/σ_D` (paired difference), the noncentrality parameter is `δ = d√N` (or `d_z√N`), with `df = N − 1`. A two-sided test uses the sum of noncentral-t upper and lower tail probabilities at critical ±`t_(1−α/2, df)`; a one-sided test uses its specified tail. The paired test assumes approximately normal **independent participant-level differences** when the sample is small.

## 3. Two independent means, including unequal groups

For pooled-SD Cohen's `d`, `δ = d√[n₁n₂/(n₁+n₂)]` and `df = n₁+n₂−2`. Power comes from the noncentral t distribution with a pooled-variance critical t threshold. Both groups must have comparable population variances; **this is not a Welch unequal-variance test**. For a given total `N`, unequal allocation generally reduces information about a two-group difference.

## 4. Pearson correlation

For the absolute target Pearson `r`, the calculator uses the **Fisher-z normal approximation**: `Z = atanh(|r|) √(N−3)`, tested against the normal critical value at α. This is approximate, especially with very small samples, non-normal data or dominant outliers. A direction-specific test uses one tail.

## 5. Factorial ANOVA, including repeated and mixed factors

The user specifies `A` factors and the *particular* main effect or interaction to detect. The effect-size helper computes an equal-cell factorial contrast component from all condition means using inclusion–exclusion of marginal means. `f` is the **root-mean-square of that targeted effect component divided by the common within-cell outcome SD at one occasion**. It is not interchangeable with a published partial-η² converted to f without verifying the underlying definition.

Let `d₁` be the product of `(levels − 1)` across the factors in the tested effect, `df_res = N−B−Q`, and `ρ` the common correlation between every pair of repeated observations. For the **complete, balanced** design (`n_b=n`), the model uses:

- Between-participant main effect or interaction: `λ = N M f²/[1 + (M−1)ρ]`, `df₁=d₁`, `df₂=df_res`.
- Effect containing at least one repeated factor: `λ = N M f²/(1−ρ)`, `df₁=d₁`, `df₂=df_res × d₁`.
- Where `M=1`, these reduce to `λ = N f²` and `df₂=N−B−Q`.
- Optional `ε<1` multiplies the repeated-effect numerator and denominator degrees of freedom. This **is only a sensitivity approximation**, because the assumed equal pairwise correlations themselves imply sphericity (`ε=1`).

### Unequal cells: deliberately conservative planning approximation

For full between-cell designs **without numerical covariates**, the beta replaces `N` by `N_eff = B × min_b(n_b)` **only in the noncentrality formula above**, while retaining `df_res=N−B`. This yields an intentionally conservative minimum-cell-information approximation relative to the balanced-cell factorial contrast scale; it does **not** implement exact unbalanced ANOVA power for an arbitrary specified means pattern, nor does it cover partial/missing combinations or heteroscedasticity. The reported power should not be read as a precise estimate under unequal allocation. For unequal factorial ANCOVA with covariates, the calculator refuses to report power, because covariate distribution and adjustment effects have not been specified.

This warning appears next to the result, in the generated summary, and in the report. In consequential studies involving complex uneven factorial allocation, a general-linear-hypothesis or simulation-based power analysis with the actual cell means and covariance specification is preferable.

## 6. Multiple linear regression and dummy-coded factors

Numerical predictors each use one coefficient; a categorical factor with `k` levels contributes `k−1` dummy-variable coefficients. Interactions include the necessary lower-order terms. For a tested block of `u` coefficients in a model with `p` slopes, `df₁=u`, `df₂=N−p−1` and the engine uses the approximate noncentral-F parameter `λ ≈ N f²`, where partial `f² = (R²_full − R²_reduced)/(1−R²_full)`. For overall model power, `u=p` and `R²_reduced=0`.

The user's `f²` must **already describe the planned predictor distribution**, including the group proportions; the engine does not recalculate partial `f²` when categorical group sizes change. Collinearity, omitted interactions, residual heteroscedasticity, repeated observations and predictor measurement error can invalidate the planning assumption.

## 7. One- and two-independent-sample proportions

The app uses Cohen's `h = 2 |asin√p₁ − asin√p₀|`; for direct h planning it reconstructs the alternative rate from a specified baseline and direction. One-sample and two-independent-proportion power use **large-sample normal approximations**, not exact binomial tests. For the two-group pooled-score-style approximation with unequal sizes, `p̄=(n₁p₀+n₂p₁)/(n₁+n₂)`, null SD `s₀=√[p̄(1−p̄)(1/n₁+1/n₂)]`, alternative SD `s₁=√[p₀(1−p₀)/n₁+p₁(1−p₁)/n₂]`, and standardized noncentral shift `δ=(p₁−p₀)/s₀`. The normal critical value uses `s₀`, while power is computed under a normal with dispersion `s₁/s₀`. Rare events and small samples require more suitable methods.

## 8. Effect-size presets, sources, and numerical checks

Conventional descriptive presets: Cohen's `d`: `.20 / .50 / .80`; Cohen's `f`: `.10 / .25 / .40`; Pearson `r`: `.10 / .30 / .50`; Cohen's `f²`: `.02 / .15 / .35`; Cohen's `h`: `.20 / .50 / .80`. They are **not substitutes for substantive effect-size justification**. The calculator also allows custom numeric values, and derivation from published means and SDs, correlations, regression model R² values and proportions. Whether the effect comes from prior research, a pilot, a minimum-important difference or an a priori planning scenario **does not change the mathematical power computation**.

Checks in `validation/gn_v1_validation.csv` compare 18 configurations against SciPy reference distribution calculations; `tests/test_unequal.py` checks a two-group 1:2 design against a noncentral t reference. These tests provide **limited numerical checking**, not certification. In particular, they cannot establish that an arbitrary user's chosen design or selected effect metric corresponds to the scientific hypothesis.

## 9. Measurement-scale guardrails

A continuous-outcome t or F model assumes that treating the dependent variable as numerical is justified; the app illustrates this with measured quantities such as systolic blood pressure (mmHg) and reaction time (milliseconds). A **single ordinal rating item** is not automatically continuous, even if its categories are represented by numbers, and this beta refuses power outputs for an outcome identified as ordinal or nominal with multiple categories. A composite scale may sometimes be modelled approximately as numerical, but this requires a separate substantive and measurement justification; GN does not diagnose it. Count outcomes, ordinal regression, multinomial models and mixed-effects analyses are not implemented.
