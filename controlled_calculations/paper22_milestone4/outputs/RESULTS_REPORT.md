# Paper 2.2 — controlled comparison results

No ground-truth file was read. No QUBO or quantum calculation was run.

The table reports the locked-test **error gate** only. The protocol also requires conflict and split-stability gates before a method can receive final task-feasible PASS status.
## SYSTEM_1_GAUSSIAN
reconstruct observed three-channel vector

| method | payload d | test RMSE | validation RMSE | error gate |
|---|---:|---:|---:|---|
| FULL | 3 | 0 | 0 | PASS |
| DIPS-5 | 3 | 0 | 0 | PASS |
| DIPS-6M | 3 | 0 | 0 | PASS |
| PCA-1 | 1 | 0.34192041 | 0.41425032 | FAIL |
| PCA-2 | 2 | 0.040517994 | 0.038614905 | PASS |
| PCA-3 | 3 | 3.5536845e-16 | 3.2261737e-16 | PASS |

## SYSTEM_2_KNOWN_FUNCTION
reconstruct current response from current/past driver only

| method | payload d | test RMSE | validation RMSE | error gate |
|---|---:|---:|---:|---|
| PCA-1 | 1 | 0.57327506 | 0.58767266 | FAIL |
| PCA-2 | 2 | 0.15543437 | 0.13012894 | FAIL |
| PCA-3 | 3 | 0.260279 | 0.16631508 | FAIL |
| PCA-4 | 4 | 0.23170006 | 0.15895171 | FAIL |
| PCA-5 | 5 | 0.240234 | 0.16216539 | FAIL |
| PCA-6 | 6 | 0.23979405 | 0.16517939 | FAIL |
| PCA-7 | 7 | 0.24280515 | 0.16619224 | FAIL |
| PCA-8 | 8 | 0.24246906 | 0.17094894 | FAIL |
| PCA-9 | 9 | 0.24211622 | 0.17351083 | FAIL |
| PCA-10 | 10 | 0.27165368 | 0.20494088 | FAIL |
| PCA-11 | 11 | 0.28535271 | 0.23757615 | FAIL |
| PCA-12 | 12 | 0.30578552 | 0.25488581 | FAIL |
| PCA-13 | 13 | 0.30149916 | 0.28113839 | FAIL |
| PCA-14 | 14 | 0.30854119 | 0.29656288 | FAIL |
| PCA-15 | 15 | 0.31324376 | 0.30523265 | FAIL |
| PCA-16 | 16 | 0.32207844 | 0.30757744 | FAIL |
| PCA-17 | 17 | 0.32967464 | 0.31043556 | FAIL |
| PCA-18 | 18 | 0.3374654 | 0.31129589 | FAIL |
| PCA-19 | 19 | 0.34252986 | 0.31327873 | FAIL |
| PCA-20 | 20 | 0.34331861 | 0.31613184 | FAIL |
| FULL-history | 21 | 0.18722067 | 0.13312179 | FAIL |
| DIPS-5 | 1 | 0.19580876 | 0.19516634 | FAIL |
| DIPS-6M | 2 | 0.09885475 | 0.10241692 | FAIL |

## SYSTEM_3_MULTIVARIATE_VECTOR
reconstruct total from retained channels

| method | payload d | test RMSE | validation RMSE | error gate |
|---|---:|---:|---:|---|
| FULL | 4 | 0 | 0 | PASS |
| DIPS-5 | 3 | 0 | 0 | PASS |
| DIPS-6M | 3 | 0 | 0 | PASS |
| PCA-1 | 1 | 0.054564999 | 0.057716679 | FAIL |
| PCA-2 | 2 | 1.1335783e-15 | 1.3944173e-15 | PASS |
| PCA-3 | 3 | 1.1506728e-15 | 1.4220577e-15 | PASS |
| PCA-4 | 4 | 1.1515805e-15 | 1.4226975e-15 | PASS |

## Interpretation boundary
An error-gate PASS is limited to its declared generator, task, typed metadata and split. It is not final certification before stability is audited. An error-gate FAIL is reported as a task failure, not as a universal failure of DIPS.