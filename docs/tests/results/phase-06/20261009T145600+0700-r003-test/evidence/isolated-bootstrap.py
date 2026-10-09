import sys
from agent_corporation_api.settings import Settings
Settings.model_config["env_file"]=None
if sys.argv[1]=="migrate":
    from alembic.config import main
    main(argv=["-c","apps/api/alembic.ini","upgrade","head"])
else:
    import pytest
    raise SystemExit(pytest.main(sys.argv[2:]))
