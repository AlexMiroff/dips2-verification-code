# Paper 2.2 — frozen controlled-analysis protocol (Milestone 2)

## Status and purpose

This document is frozen **before** any DIPS selection, parameter fitting,
baseline comparison, optimisation, QUBO construction, or quantum calculation.
It governs the three and only three controlled systems generated in Milestone 1:
`SYSTEM_1_GAUSSIAN`, `SYSTEM_2_KNOWN_FUNCTION`, and
`SYSTEM_3_MULTIVARIATE_VECTOR`.

The aim is not to claim universal compression or quantum advantage.  The aim is
to test, under declared observation contracts, whether a DIPS representation
preserves a declared task with fewer or differently structured coordinates than
the predeclared baselines, and to record explicit failures where it does not.

## Common data partition

Each 400-observation series is partitioned by time without shuffling:

| role | observations | indices |
|---|---:|---|
| representation selection / fitting | 240 | 0–239 |
| validation | 80 | 240–319 |
| locked test | 80 | 320–399 |

All admissible representations and all baselines are fitted using only the
first partition.  Choices are fixed on the validation partition.  The locked
test is evaluated once.  No method may use a latent variable, hidden memory
state, shock value, or ground-truth equation in its fitting input.

## Declared task contracts

| system | observed input | retained task | target / relation | tolerance on test |
|---|---|---|---|---:|
| SYSTEM_1_GAUSSIAN | `(x1,x2,x3)` | reconstruct each observed channel | three-channel observation vector | RMSE <= 0.10 per channel |
| SYSTEM_2_KNOWN_FUNCTION | `(u_t,y_t)` and past observations only | one-step response prediction | `y_(t+1)` | RMSE <= 0.06 |
| SYSTEM_3_MULTIVARIATE_VECTOR | `(v1,v2,v3,total)` | recover declared aggregate | `total = v1+v2-v3` | RMSE <= 1e-10 |

The tolerances are task-specific properties of these controlled generators;
they are not universal DIPS thresholds.  The Gaussian tolerance equals its
declared observation-noise scale.  The nonlinear tolerance is deliberately
larger than the bounded shock width, so the test concerns whether the required
memory structure is retained rather than whether noise is eliminated.  The
vector tolerance is numerical identity tolerance.

## Methods compared identically in every system

1. **FULL** — the complete observed vector; no reduction.  This is a fidelity
   reference, not a compression baseline.
2. **PCA-k** — principal components of standardized observed channels, with
   `k=1,...,p`, reconstructed in original units.  The selected `k` is the
   smallest validation-feasible value; otherwise `k=p` is recorded as failure
   to reduce.
3. **DIPS-5** — the declared five-coordinate DIPS grammar, with no additional
   memory coordinate.  Its grammar and each coordinate definition are written
   before fitting.
4. **DIPS-6M** — the same grammar plus exactly one declared scalar memory
   coordinate.  It is admissible only for a stated recurrence and lag order.

For the Gaussian and vector systems, a DIPS-6M result is reported but cannot
be interpreted as evidence that memory is needed unless it improves locked-test
task error by at least 10% relative to DIPS-5 *and* passes the stability rule
below.  For the known-function system, DIPS-5 and DIPS-6M directly test the
declared memory boundary.

No additional representation, neural network, hand-tuned oracle, or method
chosen after inspecting test data is admissible in this paper.

## Five reported metrics

For every `system × method`, report:

1. **Task error**: specified RMSE on the locked test, plus per-channel RMSE
   where applicable.
2. **Representation size**: number of retained scalar coordinates `d`; report
   `d/p` relative to the observed channel count `p`.  This is structural size,
   not a claimed byte-compression ratio.
3. **Conflict witnesses**: count of pairs of validation observations with the
   same reported representation (within `1e-8` after standardized coordinates)
   but task targets differing by more than the stated tolerance.  Each nonzero
   count must list the first five witness indices.
4. **Split stability**: repeat fitting on three contiguous 240-point rolling
   fitting windows where available; report maximum absolute change in task
   error.  If the system has only one full test horizon, use three 80-point
   pseudo-test blocks after each fitting segment, without revising the chosen
   model.
5. **Classical complexity**: wall-clock fitting and evaluation time, hardware
   and software versions, and a plain operation count where analytic.  It is
   descriptive only; no advantage claim follows from it.

## Decision and stopping rules

For a method to be called **task-feasible**, it must simultaneously satisfy:

- the declared locked-test tolerance;
- zero conflict witnesses under the declared rule; and
- a split-stability change no greater than 20% of its locked-test tolerance.

For a representation to be called **smaller for this task**, it must be
task-feasible and have strictly smaller `d` than the smallest task-feasible
baseline.  If a method fails any gate, the result is a STOP/FAIL, not a
near-success.  A representation that is feasible for one task or one system
is not thereby sufficient for another.

The primary comparison is: smallest task-feasible representation among FULL,
PCA-k, DIPS-5, and DIPS-6M.  Secondary comparisons report errors and witnesses
without aggregating the three systems into a single score.

## Blinding and release order

1. Implement methods against only `blind_observations.csv`.
2. Produce an immutable machine-readable results table and witness file.
3. Evaluate locked test once.
4. Only then open the corresponding `ground_truth.json` to classify the
   observed outcome as agreement, partial agreement, or disagreement with the
   controlled generator.

Ground truth may validate interpretation; it may not repair a failed method.

## Quantum admission is explicitly deferred

No quantum calculation belongs to this milestone.  A later quantum stage is
admitted only for a DIPS inverse-assignment instance that first has: a fixed
QUBO objective, exact quadratization, a penalty certificate, a known classical
optimum, a declared fidelity target (optimum, observable, or distribution),
and a predefined usefulness criterion.  A device run would be reported as a
candidate search result; it would not establish quantum advantage or quantum
necessity.

## Milestone-2 completion condition

Milestone 2 is complete when this frozen protocol, its method definitions, and
the data checksum manifest are committed as one package.  Only then may
Milestone 3 execute the declared classical comparisons.
