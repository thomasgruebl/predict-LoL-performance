from dotenv import load_dotenv
import os
import aiohttp
import asyncio


# API Rate Limits:
# 20 requests every 1 seconds(s)
# 100 requests every 2 minutes(s)


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

    async with aiohttp.ClientSession() as session:
        profile_data = await get_summoner_data(session, api_key, region, summoner_name)
        # print(profile_data)
        account_id = profile_data["accountId"]
        match_list = await get_match_list(session, api_key, region, account_id)
        # print(match_list)
        latest_match_id = match_list["matches"][0]["gameId"]
        print(latest_match_id)
        latest_match_data = await get_match_by_id(session, api_key, region, latest_match_id)
        print(latest_match_data)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
