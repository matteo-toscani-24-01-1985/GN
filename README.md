# GN — guided statistical power analysis (v1.0 beta)

**GN** is a free, browser-based tool for statistical power analysis and sample-size planning. It is intended for researchers preparing study protocols, grant proposals, preregistrations and scientific publications, as well as anyone checking the assumptions behind a reported sample-size estimate. Instead of requiring a technical test-selection workflow, the interface begins with the research design and the particular effect of interest.

**Beta notice:** This is a beta development version, **not yet fully statistically validated or peer-reviewed**. Please review the selected analysis and assumptions before using an estimate in a research protocol or publication. Complex designs may require a statistician.

## Developers and citation

**Developed by Matteo Toscani and Anna Metzger.** Contributions, author affiliations and permissions should be confirmed with both developers before manuscript submission.

The app includes an **About & cite** page accessible from the top navigation, including a provisional citation and an invitation to report bugs or contribute. For the beta, the suggested reference is:

> Toscani, M., & Metzger, A. (2026). *GN: Guided N Estimator* (Version 1.0 beta) [Computer software]. GitHub. https://github.com/matteo-toscani-24-01-1985/Nagus

This software citation is **provisional** until the beta release is publicly accessible and version details are confirmed. When a DOI is assigned, update the citation and `CITATION.cff` accordingly. Once a journal article is published, its full reference should be added; researchers may cite both the software version and the paper.

## Try it

Open **`index.html`** directly in a recent browser: the tool runs offline, with no account, data upload, or installation. Once the repository is publicly hosted on GitHub Pages, it can also be used through a website.

**GitHub source / bug reports / contributions:** **https://github.com/matteo-toscani-24-01-1985/Nagus**  
**Repository URL supplied by Matteo Toscani; public availability has not been independently verified.** The Pages address (when enabled) is `https://matteo-toscani-24-01-1985.github.io/Nagus/`. The old repository path `Nagus` is intentional; it need not match the new display name GN.

If you find a calculation error, interface bug, unclear instruction, or unsupported design, **please consider opening a GitHub issue** and include the steps needed to reproduce it (without participant-identifying data). Contributions are very welcome: code fixes, independent statistical checks, additional test cases, accessibility suggestions, examples, and documentation improvements. See `CONTRIBUTING.md` and `examples/README.md`.

## How to use it

The design-first interface asks about the dependent variable and independent predictors, numbers of factor levels, whether observations come from different or repeated participants, and the desired main effect, interaction, covariate or regression block. It then recommends a relevant test and offers numeric effect sizes plus labelled small/medium/large presets. A helper converts means/SDs and other published statistics into effects where appropriate. Power presets include 80%, 85%, 90%, 95%, 99% or any custom percentage from 1% to 99.9%.

For independent groups, choose equal allocation, a not-yet-decided allocation (plans with equal counts), or an unequal design with positive **relative weights** in each between-participant cell (e.g. 1 and 2). Repeat measurements from the same participants are never counted as new participants. The app calculates power for its selected effect, displays participants per independent group and total distinct participants, and prepares a methods-style summary. An optional recruitment adjustment allows for attrition.

## Supported designs and critical qualifications

- One-sample, independent, and paired t tests; the independent t test supports unequal group sizes **under a common-variance (pooled) assumption**.
- One-way between and repeated ANOVA, two-way and three-way independent / repeated / mixed ANOVA, and configurable N-way factorial designs with selected main effects and interactions.
- Pearson correlation (Fisher-z approximation).
- Multiple linear regression with continuous predictors, dummy-coded categorical variables and selected interaction blocks; regression power assumes the supplied partial effect size applies to the planned predictor distribution.
- One- and two-independent-proportion normal-approximate power calculations.
- **Unequal factorial ANOVA:** conservative minimum-cell approximation only, **not exact unbalanced ANOVA power**. Factorial ANCOVA with covariates and unequal cells is not supported and reports an explicit error instead of producing a misleading sample size.
- Repeated ANOVA assumes a common pairwise within-participant correlation; optional sphericity adjustment is an approximate sensitivity scenario. Ordinal/multinomial outcomes, mixed-effects models, clusters, unequal residual variances and missingness mechanisms are not implemented.

Conventional effect-size benchmarks are descriptive, and users remain responsible for a meaningful target effect. The statistical calculation is not altered according to whether that target comes from a published study or an a priori planning assumption.

## Paper and reproducibility

- `paper/manuscript.md`: short academic software description, including an invitation for beta feedback.
- `paper/technical-methods.md`: detailed formulas and qualifications for every supported test family and the allocation procedures.
- `paper/references.bib`: manuscript bibliography.
- `examples/README.md`: worked examples with clearly defined measurement scales and appropriate design assumptions.
- `validation/gn_v1_validation.csv` and `.md`: 18 independent numerical comparisons with SciPy at selected parameter settings (maximum difference <5 × 10⁻⁸); not a comprehensive validation.
- `tests/test_unequal.py`: additional numerical and UI checks of 2:1 allocation, custom power and unsupported design warnings.

## Code and tests

- `index.html`: standalone, ready-to-run single HTML file (suitable for GitHub Pages).
- `src/template.html`, `src/app.js`, `src/math.js`, `src/page.js`: editable source.
- `scripts/build.py`: rebuild `index.html` from the editable source with `python scripts/build.py`.
- `tests/validate.py`, `tests/ui_smoke.py`, `tests/test_unequal.py`, `tests/test_brand_and_scales.py`, `tests/test_about_cite.py`: optional browser and numerical checks (require Python, SciPy, Playwright and a Chromium browser).

## Before public release

Confirm the linked repository is public, authors approve their credit, affiliations are correct, and the copyright holder in `LICENSE` is confirmed. Publish the repository, enable GitHub Pages if desired, then archive a reviewed tagged version with Zenodo if an archived DOI is wanted. **No GitHub publication, journal acceptance, peer review, or DOI is claimed by this beta package.**

GN is independently branded research software; it does not use third-party franchise names or artwork.

## Name and repository path

**GN** stands for **Guided N**, where *N* denotes required sample size. The longer software name is **GN — Guided N Estimator**. The repository address deliberately retains `/Nagus` to match the user-specified GitHub location. This naming decision does not guarantee trademark availability; check for similar software names before public launch.
