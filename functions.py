import inspect

from pyrogram import Client, raw
from pyrogram.raw.functions.stories.get_boosts_status import GetBoostsStatus

from config import api_hash, api_id


def props(obj):
    pr = {}
    for name in dir(obj):
        try:
            value = getattr(obj, name)
            if not name.startswith('_') and not inspect.ismethod(value):
                pr[name] = value
        except:
            continue

    return pr


async def check_channel(channel_username: str) -> dict | str:
    async with Client(api_id=api_id,
                      api_hash=api_hash, test_mode=True,
                      name="boosteam") as app:
        try:
            channel = await app.resolve_peer(channel_username)

            if isinstance(channel, raw.types.input_peer_channel.InputPeerChannel):
                result = props(await app.invoke(
                    GetBoostsStatus(
                        peer=channel)
                ))

                response = {
                    "status": "success",
                    "chat_id": channel.channel_id,
                    "level": result["level"],
                    "boosts": result["boosts"],
                    "boost_url": result["boost_url"],
                    "next_level_boosts": result["next_level_boosts"],
                    "caption": "Success"
                }
            else:
                response = {
                    "status": "failed",
                    "caption": "This is not channel's username"
                }

            return response
        except Exception as e:
            return {"status": "error",
                    "caption": str(e)}
