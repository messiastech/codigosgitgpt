# Validação local

Executada com Python 3.12.14 no Windows. **16 testes passaram**.

Os testes cobrem reprocessamento idempotente, rollback, contratos inválidos, precisão monetária, escape HTML, ranking de busca e detecção de alterações.

A matriz no GitHub está configurada para 3.11–3.13; seu resultado remoto deve ser consultado na aba Actions.

```text
data-quality-python
test_contract_and_schema (test_app.Tests.test_contract_and_schema) ... ok
test_min_rows (test_app.Tests.test_min_rows) ... ok
test_reports_all_violations (test_app.Tests.test_reports_all_violations) ... ok
test_sample (test_app.Tests.test_sample) ... ok

----------------------------------------------------------------------
Ran 4 tests in 0.037s

OK

docsearch-python
test_failed_rebuild_preserves_index (test_app.Tests.test_failed_rebuild_preserves_index) ... ok
test_normalization (test_app.Tests.test_normalization) ... ok
test_ranking_rebuild_and_no_match (test_app.Tests.test_ranking_rebuild_and_no_match) ... ok

----------------------------------------------------------------------
Ran 3 tests in 0.124s

OK

fileguard-python
test_all_changes (test_app.Tests.test_all_changes) ... ok
test_invalid_manifest (test_app.Tests.test_invalid_manifest) ... ok
test_no_overwrite_and_nested_manifest (test_app.Tests.test_no_overwrite_and_nested_manifest) ... ok

----------------------------------------------------------------------
Ran 3 tests in 0.097s

OK

sales-insights-python
test_invalid_and_empty (test_app.Tests.test_invalid_and_empty) ... ok
test_precision_and_escape (test_app.Tests.test_precision_and_escape) ... ok
test_sample (test_app.Tests.test_sample) ... ok

----------------------------------------------------------------------
Ran 3 tests in 0.048s

OK

warehouse-etl-python
test_conflict_rolls_back_batch (test_app.Tests.test_conflict_rolls_back_batch) ... ok
test_idempotent_load (test_app.Tests.test_idempotent_load) ... ok
test_rejects_bad_rows (test_app.Tests.test_rejects_bad_rows) ... ok

----------------------------------------------------------------------
Ran 3 tests in 0.100s

OK

```
