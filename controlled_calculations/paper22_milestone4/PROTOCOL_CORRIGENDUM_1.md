# Paper 2.2 — Protocol Corrigendum 1: typed channels and numerical payload

## Why this corrigendum is required

The Milestone-2 protocol used the phrase “DIPS-5 representation size” beside
PCA component count.  This is not a valid like-for-like comparison without an
explicit adapter.  The five baseline DIPS characteristics

\[
\Phi_5=(\mathrm{source},\mathrm{receiver},\mathrm{channel},\mathrm{lag},\mathrm{strength})
\]

describe a **typed channel record**.  They are not automatically five real
coordinates replacing a time-series vector.  In particular, channel metadata
cannot be counted as a numerical reduction of measured amplitudes.

This corrigendum keeps the three systems, split, task contracts, tolerances,
baselines, stopping rules, and no-ground-truth fitting rule unchanged.  It only
makes explicit the missing bridge between the DIPS grammar and numeric data.

## Corrected representation object

For every observed channel (j) at time (t), the tested object is

\[
R_{j,t}=(\underbrace{s_j,r_j,c_j,\ell_j}_{\text{fixed typed metadata}},
          \underbrace{q_{j,t}}_{\text{observed payload}}).
\]

The fifth DIPS characteristic, `strength`, is represented by the declared
numeric payload convention (q_{j,t}): measured current magnitude for an
observed channel, or a fitted coefficient only when the declared task is a
channel-law task.  It is never replaced by hidden ground-truth quantities.

`DIPS-5` means this typed representation with no separately retained state.
`DIPS-6M` augments it only with one scalar state estimate
\(\widehat m_t\), computed causally from permitted observed history according
to a declared recurrence class.  It does not expose the true hidden memory.

## Two distinct size measures

Every result must report both quantities, never collapse them into one number.

| quantity | notation | meaning | comparison |
|---|---:|---|---|
| numeric payload dimension | `d_payload` | scalar observed/derived numeric values retained per evaluation | comparable to PCA component count |
| typed-channel description | `C_typed` | declared channel records and their five semantic fields | compared only by explicit record count and dictionary size |

A conclusion that DIPS “reduces the volume of data” is allowed only where a
declared task has a smaller feasible `d_payload`, or a smaller typed dictionary,
with the other quantity also reported.  A fixed metadata label cannot be used
as a fictitious compression gain.

## Frozen metadata declarations for the three controlled generators

These declarations come from the generator specification, not from fitted
values or the locked test.

| system | source | receiver(s) | channel | direct lag | payload convention |
|---|---|---|---|---:|---|
| SYSTEM_1_GAUSSIAN | Gaussian latent process | `x1,x2,x3` observation nodes | linear observation channel | 0 | current observed value `xj_t` |
| SYSTEM_2_KNOWN_FUNCTION | exogenous driver `u` | response node `y` | nonlinear directed response | 1 for forecasting `y_(t+1)` | current `u_t`; DIPS-6M may add a causal scalar state estimate |
| SYSTEM_3_MULTIVARIATE_VECTOR | latent vector process | `v1,v2,v3,total` observation nodes | linear composite channel | 0 | current observed value of each retained channel |

For System 2 the only admissible state-estimate class is

\[
\widehat m_{t+1}=\rho\widehat m_t+u_t,\qquad \widehat m_0=0,
\]

where \(\rho\) is selected on the 240-observation fitting partition from the
fixed grid `{-0.90,-0.85,...,0.90}`.  The state is then computed causally on
validation and locked-test partitions without reset or refitting.  This is an
observable construction; it is not the generator's hidden `m_t`.

## Admissible numerical implementations

All numerical decoders are selected on fitting data and frozen on validation.

| arm | typed information | numeric payload supplied to decoder |
|---|---|---|
| FULL | none required | all contemporaneous observed values permitted by the task contract |
| PCA-k | none required | first `k` fitted standardized principal components |
| DIPS-5 | declared records above | only the declared current payload channels; no retained scalar state |
| DIPS-6M | DIPS-5 records plus declared memory convention | DIPS-5 payload plus `m_hat_t` for System 2 only |

For each arm, the decoder class is fixed to ridge-linear prediction for linear
tasks and degree-3 ridge polynomial prediction for the nonlinear System-2
task.  Ridge penalty is selected from `10^{-8},10^{-6},10^{-4},10^{-2},1,100}`
on the validation partition.  No neural network is admitted in this small,
controlled experiment, because it would introduce an additional untested
function class rather than test the representation boundary.

## Interpretation rule

1. **System 1** tests whether the typed grammar invents a reduction where none
   is structurally warranted.  Failure to reduce is an expected legitimate
   outcome.
2. **System 2** tests the explicit boundary: whether a causal scalar memory
   state improves the declared one-step task sufficiently to pass the frozen
   gates.  A result remains task-specific.
3. **System 3** tests linked channels: whether the declared aggregate can be
   reconstructed after omitting a redundant payload channel, with the typed
   records retaining the relation's interpretation.

This is now a representation-aware comparison: numerical reduction, semantic
typing, and state augmentation are evaluated separately rather than conflated.

## Status after Corrigendum 1

The former Milestone-3 metadata blocker is resolved for these synthetic
generators.  The next admitted action is the one already planned: execute
FULL, PCA-k, DIPS-5 and DIPS-6M using these definitions, then apply the locked
test once.  No QUBO or quantum calculation is admitted.
