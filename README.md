# Boosteam Documentation Type Thing

## What is Boosteam?
Boosteam is a Telegram Mini App.

It allows you to capitalize on your Premium sub — earn TON by Boosting channels!

Likewise, Boosteam is a market you can employ Boosters on to elevate your channel. 

At Boosteam, we value boosts above subscriber count — thus, provide you with a Global Ranking based on this new metric.


![image](https://github.com/redisner/tg_boosts_miniapp/assets/128181486/ecb88353-8fa1-494f-8f39-1c3b3a8a42b2)


## Project Links:
- Telegram Mini App: [@boosteambot](https://t.me/boosteambot)
- Boosteam Channel: [@boosteamchannel](https://t.me/boosteamchannel)
- Boosteam Chat: [@boosteamchat](https://t.me/boosteamchat)

## Bot Features:
- Earn $TON for boosting other channels
- Buy boosts in bulk and improve your channel abilities
- Check how many boosts or what level does a channel have, compare it with other channels with our ranking system

Currently we have a list of top channels ranked by levels and amount of boosts being received. Trading mechanism is coming soon!

![image](https://github.com/redisner/tg_boosts_miniapp/assets/128181486/67b0c4d2-adc9-437f-a06e-ecb1ecf9f532)


## Installation Requirements:
- Python v3.10
- Python requirements from requirements.txt - can be installed with "pip install -r requirements.txt"
- PostgreSQL v14
- ~~A cup of tea to drink while installing software~~

## Code structure
- Python code
- CSS and image files for icons
- An HTML template

### APP.PY
this is a Flask web server that uses backend folder functions. Every hour all channels and their boost numbers as well as level are fetched.

### FUNCTIONS.PY
this file contains functions that checks channel by username or chat_id. this includes all the necessary info for ranking.

### BG_TASKS.PY
this file contains frequency of updates

### SQL_UTILS.PY
this python file manages all the database stuff. It operates data using PostgreSQL.
