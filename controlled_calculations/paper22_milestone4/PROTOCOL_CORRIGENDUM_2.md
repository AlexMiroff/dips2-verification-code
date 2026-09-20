# Paper 2.2 — Protocol Corrigendum 2: executable memory task

No result has been fitted or inspected under the amended task.

The original System-2 wording “predict (y_{t+1}) from present and past
observations” omitted an availability contract for the future exogenous driver
(u_{t+1}).  Such a forecast is not identified from the blind observations
unless future (u) is supplied.  Rather than introduce an undeclared oracle,
the controlled memory task is stated precisely as follows.

## Corrected System-2 task

At time (t), observe current and past driver values
\((u_t,u_{t-1},\ldots)\) and reconstruct the contemporaneous response (y_t).
The target is evaluated for (t=320,\ldots,399).  The model may not use
`y_t`, shocks, hidden memory, latent variables, or any future driver as an
input.

The comparable payloads are:

| method | input payload | dimension |
|---|---|---:|
| FULL-history | `u_t,...,u_(t-20)` | 21 |
| PCA-k | PCA encoding of that 21-lag history | k |
| DIPS-5 | direct payload `u_t` | 1 |
| DIPS-6M | `u_t,m_hat_t` under Corrigendum 1 | 2 |

All use the same degree-3 ridge decoder and frozen penalty grid.  Fitting uses
indices 20–239, validation 240–319, and locked test 320–399.  The other two
systems retain their original partitions and tasks.

This amendment preserves the scientific question: is one causally constructed
scalar state sufficient for the declared response task where a memoryless
direct channel is not?  It makes no claim about arbitrary memory models or
multi-step forecasting.
