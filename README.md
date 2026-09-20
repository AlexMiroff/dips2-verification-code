# DIPS II — Verification Code

Companion code for **"DIPS II: A Theory of Compact System Information"** (Myronov, 2026).

## Scope

The repository separates two evidential layers:

- **Theory factories** use exact rational or arbitrary-precision arithmetic to
  check finite witnesses and identities reported in the theoretical paper.
  They are implementation cross-checks; the general results rest on the stated
  proofs and domains in the article.
- **Controlled calculations** are a separate Paper 2.2 practical-methods
  programme. They are not evidence of a quantum-device result.

Install the plotting dependency once with `python3 -m pip install -r requirements.txt`. Then run a theory factory from the repository root with
`python3 factories/<filename>.py`. Every factory writes a machine-readable
JSON report. The convergence factory also creates its CSV and Figures 2–3.

## Theory factories

| Article section | Script | What it checks |
|---|---|---|
| §6.1 | `factories/section06_convergence_factory.py` | Fully specified 64-state, 1,500-replicate convergence control and Figures 2–3 |
| §§6.2, 6.4 | `factories/section06_exact_formulations_factory.py` | 800 ENUM–cover agreements, 200 ENUM–cover–QUBO agreements, and 324 Φ5/Φ6 closure tasks |
| §6 | `factories/section06_sufficiency_factory.py` | A finite six-essential-characteristic conflict witness |
| §7.7 | `factories/section07_affine_certificates_factory.py` | Nine finite certificates, horizon bounds and affine grid checks |
| §8.5 | `factories/section08_scenario_factory.py` | 69,120 linear and 69,120 offset scenario comparisons |
| §9.5 | `factories/section09_uncertainty_factory.py` | 512 generator-closure agreements and 3,060 bounded-total cases |
| §10.5 | `factories/section10_general_laws_factory.py` | 168 cycle configurations, 1,184 exact determinant evaluations, and QUBO penalty gates |
| §11.5 | `factories/section11_composition_factory.py` | Exact small-contour composition identities |
| §12.6 | `factories/section12_channel_path_factory.py` | Memory, series, feedback and shared-path identities |
| §13.6 | `factories/section13_distribution_factory.py` | Finite rational distribution laws and dependence witnesses |
| Appendix A | `appendix/theorem2_sign_law_check.py` | Theorem 2 sign-law check: 343 combinations, 0 failures |

## Saved reports and figures

The repository includes a consolidated [factory closure report](reports/factory_closure_report.json), plus the Section 6.1 [CSV](reports/section06_convergence/convergence.csv), [report](reports/section06_convergence/report.json), [Figure 2 SVG](reports/section06_convergence/figure2_convergence.svg) and [Figure 3 SVG](reports/section06_convergence/figure3_recovery.svg). These are the artifacts generated for the v17 article snapshot.

The QUBO check in §10.5 verifies a classical encoding condition only.
**No quantum device or quantum-advantage result is reported by this repository.**

## Controlled calculations

`controlled_calculations/` holds independent scripts for the companion
Paper 2.2 three-system control. Its subfolder documentation defines its scope
and status; some arms are frozen and some are exploratory diagnostics.

## License

CC BY 4.0 (Creative Commons Attribution 4.0 International), matching the
license of the article.
