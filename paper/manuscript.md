---
title: 'GN: A Guided Browser-Based Tool for Statistical Power Analysis and Sample-Size Planning'
tags:
  - statistical power
  - sample-size estimation
  - research software
  - research methods
  - open-source software
authors:
  - name: 'Matteo Toscani'
    affiliation: 1
  - name: 'Anna Metzger'
    affiliation: 2
affiliations:
  - name: 'Affiliation to be confirmed (Matteo Toscani)'
    index: 1
  - name: 'ANNA METZGER AFFILIATION — TO BE CONFIRMED'
    index: 2
bibliography: references.bib
---

# Summary

**GN** is a browser-based statistical power and sample-size calculator designed for researchers who need a practical, transparent planning tool without having to navigate technical statistical menus. The application begins by asking about the dependent variable, predictors, number of independent groups, repeated conditions, and the hypothesis of interest. It then suggests an analysis, lets users select a conventional effect-size benchmark or enter a custom value, and generates an editable, methods-style sample-size statement. Effect-size helpers accept published means and standard deviations, correlations, proportions, or regression R² information when appropriate. The application runs entirely in a modern browser, requires no account, and can be hosted as a free website or opened offline as a single HTML file.

**This is version 1.0 beta**, a development release intended for community testing and evaluation. It is **not yet a fully validated statistical package**.

# Statement of need

Sample-size justification is a routine part of research protocols, grant applications, preregistrations and scientific manuscripts. Researchers also need convenient ways to scrutinise the assumptions behind sample-size statements reported elsewhere. Widely used software such as G*Power [@faul2007] provides many analyses, and WebPower offers online power-analysis methods [@zhang2018]. However, the choice of test, its parameterisation and its assumptions may be less familiar to researchers who do not routinely conduct power calculations. Moreover, a sample-size calculation is only meaningful in relation to a defensible research question, effect magnitude, and analysis plan [@lakens2022].

GN (Guided N Estimator) therefore adopts a **design-first, hypothesis-specific interface**. It asks whether groups are independent or repeated and whether the researcher wishes to detect a main effect, a particular interaction, a covariate effect, or an overall regression effect. The software explains the meaning of that choice in ordinary language, rather than treating all effects in an ANOVA as interchangeable. This workflow is intended to support study planning and rapid independent checks of published calculations across research fields. Its usability and research impact are objectives for future evaluation, not yet established empirical outcomes.

# Functionality

The current beta supports one-sample, independent-samples, and paired t tests; one-way between-subjects and repeated-measures ANOVA; two-way, three-way, and configurable higher-order between, repeated, and mixed ANOVA; Pearson correlation; multiple linear regression with continuous predictors and dummy-coded categorical variables; and approximate tests of one or two independent proportions. The interface supports main effects, selected interactions, continuous covariates, and regression coefficient blocks, where appropriate. It explicitly declines to calculate t-test or ANOVA power for an ordinal single-item response or nominal multi-category outcome, for which the supported numerical-outcome model is inappropriate.

Target power can be selected from common values (80%, 85%, 90%, 95%, 99%) or entered as a **custom percentage**. Effect sizes can be typed directly or chosen from labelled small, medium, and large reference values displayed with their numerical definitions. These labels are conventional reference benchmarks, not evidence that a particular effect is plausible. Users may also compute appropriate effect sizes from published results. The software does not change its formula based on whether the assumed effect came from prior literature or was chosen prospectively; users can optionally record the justification.

For independent groups, users can assume equal numbers, state that the allocation has not yet been decided, or specify **unequal allocation as relative weights** for each independent between-subject cell. The two-group independent t-test calculation incorporates the actual planned group sizes. For factorial ANOVA with unequal cell counts, the beta uses a clearly identified **conservative minimum-cell approximation** rather than suggesting it implements exact general unbalanced-design power analysis. Repeated measures are counted as additional observations on the *same participants*, not additional participants. Optional expected attrition changes the recruitment target, not the power of completed observations.

# Implementation and calculations

GN is written in HTML and client-side JavaScript. It searches integer sample sizes until the power target is reached under the chosen model assumptions. The distribution engine computes probabilities using central and noncentral t or F distributions, with explicitly identified normal and Fisher-z approximations for proportions and correlation. The repeated-measures ANOVA calculations assume equal occasion-level variances and a common pairwise correlation (compound symmetry); optional sphericity adjustments are sensitivity approximations rather than a general covariance-model implementation. Regression planning uses partial Cohen f² and noncentral F approximations, with dummy-variable and interaction degrees of freedom derived from the predictor specification.

**Complete formulas, effect-size definitions, rounding rules, unequal-allocation treatment, and limits are provided in `paper/technical-methods.md`.** This supplementary note is part of the source package so that calculations can be inspected and reproduced.

# Verification and limitations

The beta includes automated browser tests and independent numerical comparisons with SciPy. Eighteen configurations of the equal-allocation statistical engine were cross-checked against reference distributions, with a maximum absolute power discrepancy below 5 × 10⁻⁸ in that set. An additional unequal-allocation check compares a 2:1 independent t-test design against the noncentral t distribution. These tests assess numerical agreement for specified inputs; **they do not constitute exhaustive validation, an evaluation of usability or research outcomes, or evidence that the model chosen by a user is appropriate**.

Important limitations include the balanced-cell standardisation of ANOVA effect sizes, the conservative unequal-cell factorial approximation, compound-symmetric repeated-measure assumptions, lack of mixed-effects and clustered-sample models, assumptions of equal residual variances, and omission of automatic multiplicity correction. Estimates remain sensitive to the assumed effect size, covariate structure, and recruitment process. The generated reporting text must be reviewed by a researcher before inclusion in a proposal or publication.

# Development team and citation

**GN was developed by Matteo Toscani and Anna Metzger.** Author affiliations, contribution statements and manuscript approval remain to be confirmed before submission. The software's About & cite page and `CITATION.cff` provide a provisional beta citation. Once a public code release or archival DOI is available, the citation metadata will be updated. If the accompanying software paper is subsequently published, its journal reference will be added separately; citing the actual software version remains useful for reproducibility.

# Availability, feedback, and contributions

The project repository URL is **[GN on GitHub](https://github.com/matteo-toscani-24-01-1985/Nagus)** (URL supplied by the project owner; public accessibility and current contents should be checked before release). The public site can subsequently be hosted via GitHub Pages, with an archived release and DOI created only after the software and documentation have been reviewed.

As **GN v1.0 beta** is under active development, users who encounter incorrect results, technical bugs, confusing instructions, or missing design cases are **warmly invited to open a GitHub issue** with a reproducible example. Suggestions, independent numerical checks, documentation improvements, and code contributions are also welcome through the repository. Such reports will help improve accuracy, clarity, and accessibility ahead of a stable release. The copyright line in the bundled MIT license still requires confirmation by the developers; no Zenodo DOI or peer-review status is claimed.

# AI assistance disclosure

Generative AI assisted in prototyping the application and drafting supporting material. Before submission, the human authors should review the code, independently validate statistical methods, verify literature references, establish authorship and licensing, and provide the AI disclosure required by the receiving journal.
