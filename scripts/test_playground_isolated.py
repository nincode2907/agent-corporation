"""Test on a fresh named database/role; never resets the app database or calls AI."""
import os
from pathlib import Path
import re
import subprocess
import sys
from uuid import uuid4

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'apps/api/src'))
from sqlalchemy import create_engine
from sqlalchemy.engine import make_url
from agent_corporation_api.settings import get_settings


def main():
    settings = get_settings()
    source = make_url(settings.migration_database_url or settings.database_url)
    suffix = uuid4().hex[:16]
    database, role, password = 'ac_pgtest_' + suffix, 'ac_pgtest_' + suffix, uuid4().hex + uuid4().hex
    assert re.fullmatch(r'ac_pgtest_[a-f0-9]{16}', database) and role == database
    admin = create_engine(source, isolation_level='AUTOCOMMIT')
    env = os.environ.copy()
    env.update(DATABASE_URL=source.set(database=database, username=role, password=password).render_as_string(hide_password=False),
               MIGRATION_DATABASE_URL=source.set(database=database).render_as_string(hide_password=False),
               APP_DATABASE_USER=role, APP_DATABASE_PASSWORD=password, PLAYGROUND_TEST_ISOLATED='1',
               PHASE_RUNTIME_TEST_ISOLATED='1', PLAYGROUND_WORKER_ENABLED='false', PYTHONUTF8='1')
    created = False
    try:
        with admin.connect() as db:
            db.exec_driver_sql(f'CREATE DATABASE "{database}"')
            created = True
        commands = [
            ['rtk', 'proxy', sys.executable, '-m', 'alembic', '-c', 'apps/api/alembic.ini', 'upgrade', 'head'],
            ['rtk', 'proxy', sys.executable, '-m', 'pytest', 'apps/api/tests', '-q'],
        ]
        for command in commands:
            result = subprocess.run(command, env=env, capture_output=True, text=True, encoding='utf-8', errors='replace')
            output = result.stdout + result.stderr
            for value in (password, settings.app_database_password, source.password):
                if value:
                    output = output.replace(value, '[REDACTED]')
            print(output, flush=True)
            if result.returncode:
                return result.returncode
        return 0
    finally:
        with admin.connect() as db:
            if created:
                db.exec_driver_sql(f'DROP DATABASE "{database}" WITH (FORCE)')
            db.exec_driver_sql(f'DROP ROLE IF EXISTS "{role}"')
        admin.dispose()
        print('Disposable Playground test database/role removed; runtime data unchanged.', flush=True)


if __name__ == '__main__':
    raise SystemExit(main())
