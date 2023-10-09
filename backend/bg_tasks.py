import asyncio

from backend.sql_utils import get, Channel, add, Boost
from backend.functions import check_channel


def periodic_check():
    channels = asyncio.run(get(Channel, None, None))
    for channel in channels:
        result = asyncio.run(check_channel(channel.username))

        if result["status"] == "success":
            asyncio.run(add(Boost, [{
                "channel_id": channel.id,
                "boosts_count": result["boosts"],
                "level": result["level"],
                "left_to_level_up": result["next_level_boosts"]
            }]))
