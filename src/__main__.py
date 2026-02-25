"""Allow running with python -m src."""

import asyncio

from src.bot import main

asyncio.run(main())
