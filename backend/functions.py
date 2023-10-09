import inspect
import types

from pyrogram import Client, raw
from pyrogram.raw.functions.stories.get_boosts_status import GetBoostsStatus
from pyrogram.raw.functions.contacts.search import Search
from pyrogram.raw.types import InputPeerChannel

from backend.config import api_hash, api_id


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


async def check_channel(channel_username: str | None = None,
                        chat_id: int | None = None) -> dict | str:
    async with Client(api_id=api_id,
                      api_hash=api_hash,
                      name="boosteam") as app:
        try:
            if chat_id is not None:
                channel = await app.resolve_peer(int(str(chat_id)[4:]))
            elif channel_username is not None:
                results = (await app.invoke(Search(q=f"@{channel_username}", limit=1))).chats
                channel = None
                for result in results:
                    if isinstance(result, raw.types.Channel):
                        if any(username == channel_username for username in result.usernames) or result.username == channel_username:
                            channel = result

            if isinstance(channel, raw.types.input_peer_channel.InputPeerChannel | raw.types.Channel):
                result = props(await app.invoke(
                    GetBoostsStatus(
                        peer=InputPeerChannel(channel_id=channel.id,
                                              access_hash=channel.access_hash))
                ))

                response = {
                    "status": "success",
                    "username": channel.username or channel.usernames[0],
                    "chat_id": channel.id,
                    "level": result["level"],
                    "boosts": result["boosts"],
                    "boost_url": result["boost_url"],
                    "next_level_boosts": result["next_level_boosts"],
                    "access_hash": channel.access_hash,
                    "caption": "Success"
                }
            else:
                response = {
                    "status": "failed",
                    "caption": "This is not channel's username nor chat_id"
                }

            return response
        except Exception as e:
            return {"status": "error",
                    "caption": str(e)}
