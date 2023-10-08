from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask, request

from bg_tasks import periodic_check
from sql_utils import add, Channel, get, Boost
from functions import check_channel

schedule = BackgroundScheduler(daemon=True)
schedule.add_job(periodic_check, 'interval', hours=1)
schedule.start()

app = Flask(__name__)


@app.route('/check_boosts')
async def check_boosts_endpoint():
    username = request.args.get("username")

    if username:
        if "@" in username:
            username = username.split("@")[1]
        elif "t.me/" in username:
            username = username.split("t.me/")[1]

        sql_channel = await get(Channel, "username", username)

        if sql_channel is None:
            result = await check_channel(username)

            if result["status"] == "success":
                await add(Channel, [{
                    "chat_id": result["chat_id"],
                    "username": username
                }])

                sql_channel = await get(Channel, "username", username)

                await add(Boost, [{
                    "channel_id": sql_channel.id,
                    "boosts_count": result["boosts"],
                    "level": result["level"],
                    "left_to_level_up": result["next_level_boosts"]
                }])
        else:
            result = {
                "status": "success",
                "caption": "Success",
                "boost_url": f"https://t.me/{username}?boost",
                "chat_id": sql_channel.chat_id
            }

            boosts = await get(Boost, "channel_id", sql_channel.id)

            for last_boost in boosts:
                result["boosts"] = last_boost.boosts_count,
                result["level"] = last_boost.level
                result["next_level_boosts"] = last_boost.left_to_level_up

                break
    else:
        result = {
            "status": "error",
            "caption": "Username is missing"
        }

    return result


if __name__ == '__main__':
    app.run()
