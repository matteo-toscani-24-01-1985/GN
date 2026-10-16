# GN v1.0 beta — Numerical cross-checks

18 distinct design/effect combinations checked against SciPy 1.17.0 reference distributions. Maximum absolute power discrepancy in this set: 4.9e-08.

These checks compare computed power at the app-selected sample size. They do not constitute comprehensive validation of software behavior, unbalanced or heteroscedastic designs, repeated covariance assumptions, applicability to real research designs, or educational utility.

| Case | Sample | Browser power | SciPy power | Absolute difference |
|---|---:|---:|---:|---:|
| independent_t | 128 | 0.801460 | 0.801460 | 3.5e-08 |
| one_sample_t | 34 | 0.807778 | 0.807778 | 7.7e-09 |
| paired_t | 34 | 0.807778 | 0.807778 | 7.7e-09 |
| one_way_between | 159 | 0.804887 | 0.804887 | 8.2e-15 |
| one_way_repeated | 28 | 0.812455 | 0.812455 | 1.6e-14 |
| one_way_repeated_rho80 | 12 | 0.806482 | 0.806482 | 1.8e-14 |
| two_between_main | 128 | 0.801362 | 0.801362 | 9.5e-15 |
| two_between_interaction | 128 | 0.801362 | 0.801362 | 9.5e-15 |
| two_mixed_main_A | 86 | 0.801472 | 0.801472 | 4.1e-15 |
| two_mixed_main_Time | 28 | 0.811560 | 0.811560 | 1.9e-14 |
| two_mixed_interaction | 28 | 0.811560 | 0.811560 | 1.9e-14 |
| three_within_main | 10 | 0.803097 | 0.803097 | 3.8e-15 |
| three_mixed_threeway | 28 | 0.809540 | 0.809540 | 1.6e-14 |
| regression_overall | 77 | 0.801766 | 0.801766 | 4.8e-15 |
| regression_covariate | 55 | 0.804512 | 0.804512 | 5.6e-16 |
| regression_dummy_factor | 72 | 0.827973 | 0.827973 | 5.9e-15 |
| regression_dummy_interaction | 72 | 0.827400 | 0.827400 | 6e-15 |
| correlation | 85 | 0.800346 | 0.800346 | 4.9e-08 |

## Approximations / definitions
- t tests: two-sided noncentral t.
- ANOVA: univariate, balanced, equal within-occasion variance and compound-symmetric repeated covariance, noncentral F.
- Regressions: block F with lambda = N*f² and p = design-matrix parameter count; covariate correlations are not separately specified.
- Correlation: Fisher z large-sample approximation, reproduced at the same approximation in SciPy.
- Binary rates use a normal approximation; full coverage deferred.
