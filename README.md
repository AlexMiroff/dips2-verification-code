# DIPS II — Verification Code

Companion code for **"DIPS II: A Theory of Compact System Information"** (Myronov, 2026).

## Scope

The repository separates two evidential layers:

- **Theory factories** use exact rational or arbitrary-precision arithmetic to
  check the finite witnesses and identities reported in the theoretical paper.
  They are implementation cross-checks; the general results rest on the stated
  proofs and domains in the article.
- **Controlled calculations** are a separate Paper 2.2 practical-methods
  programme. They are not evidence of a quantum-device result.

All theory factories use only the Python standard library. Run them from the
repository root with `python3 factories/<filename>.py`. Each produces a JSON
report alongside the script.

## Theory factories

| Article section | Script | What it checks |
|---|---|---|
| §6 | `factories/section06_sufficiency_factory.py` | A finite six-essential-characteristic conflict witness |
| §10.5 | `factories/section10_general_laws_factory.py` | 168 cycle configurations, 1,184 exact determinant evaluations, and QUBO penalty gates |
| §11.5 | `factories/section11_composition_factory.py` | Exact small-contour composition identities |
| §12.6 | `factories/section12_channel_path_factory.py` | Memory, series, feedback and shared-path identities |
| §13.6 | `factories/section13_distribution_factory.py` | Finite rational distribution laws and dependence witnesses |
| Appendix A | `appendix/theorem2_sign_law_check.py` | Theorem 2 sign-law check: 343 combinations, 0 failures |

The QUBO check in §10.5 verifies a classical encoding condition only.
**No quantum device or quantum-advantage result is reported by this repository.**

## Controlled calculations

`controlled_calculations/` holds independent scripts for the companion
Paper 2.2 three-system control. Its subfolder documentation defines its scope
and status; some arms are frozen and some are exploratory diagnostics.

## License

CC BY 4.0 (Creative Commons Attribution 4.0 International), matching the
license of the article.
