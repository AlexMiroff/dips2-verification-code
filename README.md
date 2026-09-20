# DIPS II — Verification Code

Companion code for **"DIPS II: A Theory of Compact System Information"** (Myronov, 2026).

## Contents

### `appendix/theorem2_sign_law_check.py`
Exact high-precision numerical verification of Theorem 2 (global sign law for
complementary power maps), as printed in Appendix A of the article. Uses only
the Python standard library (`decimal`), 180-digit precision.

Reproduces the article's claim of 343 tested combinations with 0 failures:

```
$ python3 theorem2_sign_law_check.py
343 0
```

### `controlled_calculations/`
Independent controlled-calculation scripts for the companion practical-methods
work (Paper 2.2 / three-system control), included here for transparency since
they are referenced by the same research programme. See the inline README
notes in each subfolder for scope and status (some arms are frozen, some are
exploratory diagnostics, clearly labeled as such in their own output files).

## License

CC BY 4.0 (Creative Commons Attribution 4.0 International), matching the
license of the article.

## Status

This repository is a work in progress. Additional verification scripts
referenced in the article (Sections 6, 10.5, 11.5, 12.6, 13.6) will be added
as they are prepared for independent release.
