"""Shared default shelter hours and booking settings (code, migrations, tests)."""

import datetime

DEFAULT_SHELTER_OPEN = datetime.time(8, 0)
DEFAULT_SHELTER_CLOSE = datetime.time(18, 0)
DEFAULT_SLOT_STEP_MINUTES = 15
