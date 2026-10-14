import sys, os, json
from pathlib import Path
sys.path.insert(0,str(Path('apps/api/src').resolve()))
from agent_corporation_api import settings
settings.get_settings=lambda:settings.Settings(_env_file=None,database_url='postgresql+psycopg://agent_corporation_app:fixture_only_app@127.0.0.1:15591/qa_p05',migration_database_url='postgresql+psycopg://qa_owner:fixture_only_p05@127.0.0.1:15591/qa_p05',app_database_password='fixture_only_app')
from alembic.config import Config
from alembic import command
command.upgrade(Config('apps/api/alembic.ini'),'head')
print('Migration isolated PostgreSQL: head 20261009_0007')
os.environ['PHASE_RUNTIME_TEST_ISOLATED']='1'
import pytest
raise SystemExit(pytest.main(['-q','apps/api/tests/test_codex_gateway.py','apps/api/tests/test_owner_auth.py','apps/api/tests/test_phase06_runtime.py','apps/api/tests/test_phase06_runtime_persistence.py']))
