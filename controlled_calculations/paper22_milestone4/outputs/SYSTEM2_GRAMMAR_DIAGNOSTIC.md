# System 2 — grammar diagnostic

This is a separately labelled exploratory audit and does not replace the frozen polynomial-ridge main comparison.

- **status**: `EXPLORATORY_GRAMMAR_AUDIT_NOT_MAIN_COMPARISON`
- **family**: `a*tanh(b*u+c*m_hat+d)+e`
- **rho_selected_on_validation**: `0.65`
- **parameters_fitted_on_training**: `[1.0010624524026075, 0.8919190646315454, 0.7037204515895922, -0.0018138421057431891, -0.00015609067932579901]`
- **validation_rmse**: `0.011503093659286374`
- **locked_test_rmse**: `0.011501604931518293`
- **error_tolerance**: `0.06`
- **error_gate_pass**: `True`
- **uses_ground_truth_file**: `False`
- **uses_quantum**: `False`
- **stability_windows**: `{'early_train_20_239_eval_240_319_rmse': 0.011503093659286374, 'late_train_100_319_eval_320_399_rmse': 0.011570956743392855, 'absolute_change': 6.786308410648006e-05, 'allowable_change': 0.012, 'stability_gate_pass': True}`