import asyncio
import random

from backend.sql_utils import get, Channel, add, Boost
from backend.functions import update_boosts


def periodic_check():
    channels = asyncio.run(get(Channel, None, None))
    for channel in channels:
        result = asyncio.run(update_boosts(channel.chat_id))

        if result["status"] == "success":
            asyncio.run(add(Boost, [{
                "channel_id": channel.id,
                "boosts_count": result["boosts"],
                "level": result["level"],
                "left_to_level_up": result["next_level_boosts"]
            }]))

        asyncio.run(asyncio.sleep(random.randint(500, 1000) / 100))
