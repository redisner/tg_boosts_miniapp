# -*- coding: utf-8 -*-

import base64
import inspect
import os

import pyrogram
from pyrogram import Client, raw
from pyrogram.raw.functions.stories.get_boosts_status import GetBoostsStatus
from pyrogram.raw.functions.contacts.search import Search
from pyrogram.raw.types import InputPeerChannel

from backend.config import api_hash, api_id
from backend.sql_utils import Channel, get


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
                channel = None
                try:
                    async for msg in app.get_chat_history(channel_username, limit=1):
                        channel = msg.chat
                except Exception as e:
                    print(e)
                    results = (await app.invoke(Search(q=f"@{channel_username}", limit=1))).chats
                    for result in results:
                        if isinstance(result, raw.types.Channel):
                            if any(username == channel_username for username in
                                   result.usernames) or result.username == channel_username:
                                channel = result

            if isinstance(channel, raw.types.Channel) or \
                    (isinstance(channel, pyrogram.types.user_and_chats.chat.Chat)
                     and str(channel.type) == "ChatType.CHANNEL"):

                c_id = int(str(channel.id).split("-100")[1])
                c_username = channel.username or channel.usernames[0].username

                access_hash = (await app.resolve_peer(channel.id)).access_hash

                photo = await app.download_media(channel.photo.small_file_id)
                encoded_string = str(base64.b64encode(open(photo, "rb").read())).split("'")[1]
                os.remove(photo)

                result = props(await app.invoke(
                    GetBoostsStatus(
                        peer=InputPeerChannel(channel_id=c_id,
                                              access_hash=access_hash))
                ))

                response = {
                    "status": "success",
                    "username": c_username,
                    "chat_id": c_id,
                    "level": result["level"],
                    "boosts": result["boosts"],
                    "boost_url": result["boost_url"],
                    "next_level_boosts": result["next_level_boosts"],
                    "name": channel.title,
                    "access_hash": access_hash,
                    "picture": encoded_string,
                    "caption": "Success"
                }
            elif channel is None:
                response = {
                    "status": "failed",
                    "caption": "Can't find channel"
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


async def update_boosts(chat_id: int):
    async with Client(api_id=api_id,
                      api_hash=api_hash,
                      name="boosteam") as app:
        sql_channel = await get(Channel, "chat_id", chat_id)

        result = props(await app.invoke(
            GetBoostsStatus(
                peer=InputPeerChannel(channel_id=chat_id,
                                      access_hash=int(sql_channel.access_hash)))
        ))

        print(result)

        return {
            "status": "success",
            "level": result["level"],
            "boosts": result["boosts"],
            "boost_url": result["boost_url"],
            "next_level_boosts": result["next_level_boosts"],
            "caption": "Success"
        }
