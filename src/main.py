import pymongo
from dotenv import load_dotenv
from pymongo import MongoClient
import os
import aiohttp
import asyncio


# API Rate Limits:
# 20 requests every 1 seconds(s)
# 100 requests every 2 minutes(s)

def connect_database(db_user, db_pw, db_name):

    # .env file:

    # DB_USER = "predlol_user"
    # DB_PW = "c75nvUxhcdQNYrlM"
    # DB_NAME = "predlol"

    try:
        cluster = MongoClient(
            "mongodb+srv://" +
            db_user +
            ":" +
            db_pw +
            "@cluster0.qxngf.mongodb.net/" +
            db_name +
            "?retryWrites=true&w=majority"
        )

        db = cluster["predlol"]
        collection = db["python"]

        # test
        test_post = {"gameId": 0, "match_data": "empty"}
        collection.insert_one(test_post)

    except Exception as e:
        print("Connection Error %d: %s" % (e.args[0], e.args[1]))


async def get_summoner_data(session, api_key, region, summoner_name):
    async with session.get(
        "https://" +
        region +
        ".api.riotgames.com/lol/summoner/v4/summoners/by-name/" +
        summoner_name +
        "?api_key=" +
        api_key
    ) as resp:
        data = await resp.json()
        return data


async def get_match_list(session, api_key, region, account_id):
    async with session.get(
        "https://" +
        region +
        ".api.riotgames.com/lol/match/v4/matchlists/by-account/" +
        account_id +
        "?api_key=" +
        api_key
    ) as resp:
        data = await resp.json()
        return data


async def get_match_by_id(session, api_key, region, match_id):
    async with session.get(
        "https://" +
        region +
        ".api.riotgames.com/lol/match/v4/matches/" +
        str(match_id) +
        "?api_key=" +
        api_key
    ) as resp:
        data = await resp.json()
        return data


async def main():
    load_dotenv()

    api_key = os.getenv("PREDLOL_API_KEY")
    summoner_name = os.getenv("PREDLOL_SUMMONER_NAME")
    region = os.getenv("PREDLOL_REGION")

    db_user = os.getenv("DB_USER")
    db_pw = os.getenv("DB_PW")
    db_name = os.getenv("DB_NAME")

    connect_database(db_user, db_pw, db_name)

    async with aiohttp.ClientSession() as session:
        profile_data = await get_summoner_data(session, api_key, region, summoner_name)
        # print(profile_data)
        account_id = profile_data["accountId"]
        match_list = await get_match_list(session, api_key, region, account_id)
        # print(match_list)

        # get latest match
        latest_match_id = match_list["matches"][0]["gameId"]
        print(latest_match_id)
        latest_match_data = await get_match_by_id(session, api_key, region, latest_match_id)
        print(latest_match_data)

        # get last ~100 matches
        game_ids = list()
        game_ids = [match['gameId'] for match in match_list['matches']]
        game_ids = game_ids[:95]

        for game_id in game_ids:
            match_data = await get_match_by_id(session, api_key, region, game_id)
            print(match_data)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
