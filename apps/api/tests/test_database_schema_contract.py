from agent_corporation_api.database import REQUIRED_SCHEMA_COLUMNS, missing_schema_elements


def test_schema_contract_requires_phase_0010_reconciliation_table():
    actual = {table: set(columns) for table, columns in REQUIRED_SCHEMA_COLUMNS.items()}
    actual.pop("runtime_reconciliation_decisions")
    missing = missing_schema_elements(actual)
    assert "table:runtime_reconciliation_decisions" in missing


def test_schema_contract_identifies_missing_required_column():
    actual = {table: set(columns) for table, columns in REQUIRED_SCHEMA_COLUMNS.items()}
    actual["runtime_reconciliation_decisions"].remove("request_hash")
    assert "column:runtime_reconciliation_decisions.request_hash" in missing_schema_elements(actual)


def test_schema_contract_accepts_all_required_relations_and_columns():
    actual = {table: set(columns) for table, columns in REQUIRED_SCHEMA_COLUMNS.items()}
    assert missing_schema_elements(actual) == []


def test_employee_version_identity_is_required_on_the_base_run_relation():
    assert "employee_version_id" in REQUIRED_SCHEMA_COLUMNS["runs"]
    assert "employee_version_id" not in REQUIRED_SCHEMA_COLUMNS["runtime_runs"]
