from datetime import datetime

API_KEY = "RGAPI-892688c6-0227-4ae9-907b-c9480e67e880"
LOL_REGION = "euw1"
SUMMONER = "Horns342"


def GET_API_KEY():
    return API_KEY


def GET_REGION():
    return LOL_REGION


def GET_SUMMONER():
    return SUMMONER


def unixtime_extract_day(unixtime):
    return datetime.utcfromtimestamp(unixtime).strftime('%A')