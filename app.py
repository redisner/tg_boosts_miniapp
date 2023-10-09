from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask, request, render_template

from backend.bg_tasks import periodic_check
from backend.sql_utils import add, Channel, get, Boost, custom_query
from backend.functions import check_channel, props

schedule = BackgroundScheduler(daemon=True)
schedule.add_job(periodic_check, 'interval', hours=1)
schedule.start()

app = Flask(__name__)


@app.route('/check_boosts')
async def check_boosts_endpoint():
    username = request.args.get("username")
    chat_id = request.args.get("chat_id")

    if not (username or chat_id):
        return {
            "status": "error",
            "caption": "Username or chat_id is missing"
        }

    sql_channel = None

    if chat_id:
        if "-100" in chat_id:
            chat_id = int(chat_id.split("-100")[1])
        sql_channel = await get(Channel, "chat_id", chat_id)

    if username:
        if "@" in username:
            username = username.split("@")[1]
        elif "t.me/" in username:
            username = username.split("t.me/")[1]

        sql_channel = await get(Channel, "username", username)

    if sql_channel is None:
        result = await check_channel(username, chat_id)

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

    return result


@app.route("/get_ranking")
async def get_ranking_endpoint():
    boosts = await custom_query("""select (row_number() over (), a.*) from (select c.username, max(b.boosts_count) as boosts_cnt, b.level, b.check_time
from boosts b join channels c on c.id = b.channel_id
group by c.username, b.check_time, b.level order by boosts_cnt desc limit 10) a""")

    result = []

    prepared = [str(x)[1:-1].split(",") for x in boosts]

    for boost in prepared:
        result += [
            {
                "username": boost[1],
                "place": boost[0],
                "pic": "boosts.png",
                "boosts": boost[2],
                "level": boost[3]
            }
        ]

    return result


@app.route("/")
async def mini_app():
    return render_template("index.html")


if __name__ == '__main__':
    app.run()
