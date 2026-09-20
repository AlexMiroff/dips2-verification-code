# Paper 2.2 — DIPS execution admission gate (Milestone 3)

## Result

**Status: BLOCKED before fitting.**  The three numerical control datasets are
valid for their stated prediction/reconstruction tasks, but do not yet define a
source-resolved DIPS realization.  Consequently, executing a method labelled
`DIPS-5` or `DIPS-6M` on them would require inventing the five baseline
characteristics after the data have been seen.  That would violate the frozen
protocol and would not test the five-coordinate DIPS baseline of Paper 1.

This is a positive methodological result, not an absence of work: it
demonstrates that a feature vector is not automatically a DIPS realization.
Representation-aware DIPS requires the system, observation contract,
representation, grammar, and task to be distinguished before sufficiency is
tested.

## Why the current files are insufficient

The Paper-1 baseline is

`Φ₅ = (source, receiver, channel, lag, strength)`.

Milestone-1 blind files provide only the following fields:

| system | fields in blind file | missing for a Φ₅ realization |
|---|---|---|
| SYSTEM_1_GAUSSIAN | `t,x1,x2,x3` | source, receiver, channel semantics, and an operational lag convention |
| SYSTEM_2_KNOWN_FUNCTION | `t,u,y` | source/receiver identity and a declared distinction between direct lag and stored state |
| SYSTEM_3_MULTIVARIATE_VECTOR | `t,v1,v2,v3,total` | source/receiver identity, channel semantics, and whether the aggregate is an observation or a task output |

The variables can be given names such as “x1 channel”, but names alone do not
provide a source-resolved channel relation.  Conversely, fitting a generic
five-dimensional transform to these columns would be a new feature-engineering
method, not the stated DIPS grammar.

## What must be declared — once, before any DIPS fit

For each observed channel (j), add a fixed metadata row:

| required field | meaning | permitted source |
|---|---|---|
| `source_j` | origin entity/state/process | generator specification, not fitted data |
| `receiver_j` | receiving entity/state/process | generator specification, not fitted data |
| `channel_j` | operational mechanism/type | generator specification, not fitted data |
| `lag_j` | direct transmission delay convention | generator specification, not selected from test data |
| `strength_j` | declared quantity or parameter represented by the observed value | generator specification; numerical value from the blind file only |
| `task_j` | output that must be preserved | already frozen in Milestone 2 |

For `SYSTEM_2_KNOWN_FUNCTION`, one further row is required:

| field | required declaration |
|---|---|
| `memory` | whether (m_t) is a system state distinct from direct lag, its scalar recurrence class, and which observed history is permitted to estimate it |

The declaration must be made from the known controlled generator, sealed with
the protocol, and never tuned to locked-test output.  It is metadata, not
access to hidden numerical states, shocks, or latent variables.

## Consequence for the frozen comparison

The protocol's FULL and PCA-k arms remain executable as generic numerical
baselines.  The DIPS-5 and DIPS-6M arms are **not admitted** until the metadata
above is supplied.  Running only FULL/PCA would not answer the paper's DIPS
question, so no partial “DIPS versus baseline” score is released.

When the metadata is declared, the frozen split, metrics, tolerances, stopping
rules and exactly-three-system scope remain unchanged.  The next admissible
action is then to implement the four already-announced arms and evaluate the
locked test once.

## What this does and does not imply

- It does **not** show that DIPS-5 fails.
- It does **not** show that DIPS-6M is needed.
- It does show that neither assertion is identified by the present numerical
  files without a declared DIPS observation contract.
- It preserves the result of Paper 2.1: Φ₅ is a task-relative baseline, and a
  memory coordinate is required only when a declared task has a conflict
  witness that the baseline cannot separate.

## Required status in Paper 2.2 work log

`SYSTEM_1_GAUSSIAN: BLOCKED — DIPS metadata absent.`

`SYSTEM_2_KNOWN_FUNCTION: BLOCKED — DIPS metadata and observable-memory convention absent.`

`SYSTEM_3_MULTIVARIATE_VECTOR: BLOCKED — DIPS metadata absent.`

No optimisation, QUBO, or quantum calculation has been started.
