import asyncio
from surrealdb import Surreal
from indexer import TopicIndexer
from dotenv import load_dotenv
from os import getenv

CATEGORIES = { # thank you jeffalo :3
    1: {"name": "Suggestions", "user_accessible": True},
    2: {"name": "Dustbin", "user_accessible": False},
    3: {"name": "Bugs and Glitches", "user_accessible": True},
    4: {"name": "Questions about Scratch", "user_accessible": True},
    5: {"name": "Announcements", "user_accessible": True},
    6: {"name": "New Scratchers", "user_accessible": True},
    7: {"name": "Help With Scripts", "user_accessible": True},
    8: {"name": "Show and Tell", "user_accessible": True},
    9: {"name": "Project Ideas", "user_accessible": True},
    10: {"name": "Collaboration", "user_accessible": True},
    11: {"name": "Requests", "user_accessible": True},
    12: {"name": "Moderators", "user_accessible": False},
    13: {"name": "Deutsch", "user_accessible": True},
    14: {"name": "Español", "user_accessible": True},
    15: {"name": "Français", "user_accessible": True},
    16: {"name": "中文", "user_accessible": True},
    17: {"name": "Polski", "user_accessible": True},
    18: {"name": "日本語", "user_accessible": True},
    19: {"name": "Nederlands", "user_accessible": True},
    20: {"name": "Português", "user_accessible": True},
    21: {"name": "Italiano", "user_accessible": True},
    22: {"name": "עברית", "user_accessible": True},
    23: {"name": "한국어", "user_accessible": True},
    24: {"name": "Norsk", "user_accessible": True},
    25: {"name": "Türkçe", "user_accessible": True},
    26: {"name": "Ελληνικά", "user_accessible": True},
    27: {"name": "Pусский", "user_accessible": True},
    28: {"name": "Translating Scratch", "user_accessible": True},
    29: {"name": "Things I'm Making and Creating", "user_accessible": True},
    30: {"name": "Things I'm Reading and Playing", "user_accessible": True},
    31: {"name": "Advanced Topics", "user_accessible": True},
    32: {"name": "Connecting to the Physical World", "user_accessible": True},
    33: {"name": "Català", "user_accessible": True},
    34: {"name": "Other Languages", "user_accessible": True},
    35: {"name": "Mentors Forum", "user_accessible": False},
    36: {"name": "Bahasa Indonesia", "user_accessible": True},
    37: {"name": "Scratch Day 2014", "user_accessible": False},
    38: {"name": "Spam Dustbin", "user_accessible": False},
    39: {"name": "Scratch Helper Groups", "user_accessible": False},
    40: {"name": "Camp Counselor Forum", "user_accessible": False},
    41: {"name": "Extension Developer's Forum ", "user_accessible": False},
    42: {"name": "Scratch Stability Team Forum", "user_accessible": False},
    44: {"name": "Scratch Day 2015", "user_accessible": False},
    46: {"name": "Scratch Design Studio Forum ", "user_accessible": False},
    48: {"name": "Developing Scratch Extensions", "user_accessible": True},
    49: {"name": "Open Source Projects", "user_accessible": True},
    50: {"name": "Welcoming Committee", "user_accessible": False},
    51: {"name": "Community Blocks Forum", "user_accessible": False},
    52: {"name": "Scratch Day 2016", "user_accessible": False},
    54: {"name": "Scratch Day 2017", "user_accessible": False},
    55: {"name": "Africa", "user_accessible": True},
    56: {"name": "Scratch Day 2018", "user_accessible": False},
    57: {"name": "Scratch 3.0 Beta", "user_accessible": False},
    58: {"name": "Camp Counselors 2020", "user_accessible": False},
    59: {"name": "فارسی", "user_accessible": True},
    60: {"name": "Project Save & Level Codes", "user_accessible": True},
    61: {
        "name": "April Fools Day - Suggest-Show-Question-Bugs-Help-Glitch-Tell-Etc",
        "user_accessible": False,
    },
}

async def main():
    load_dotenv()
    db = Surreal("ws://127.0.0.1:8000/rpc")
    await db.connect()
    await db.use(namespace="Voyager", database="Voyager")
    await db.signin({"user": getenv("USERNAME"), "pass": getenv("PASSWORD")})
    indexer = TopicIndexer(db)
    indexed_categories = [
        await indexer._index_category(category_id)
        for category_id, category in CATEGORIES.items() 
        if category["user_accessible"]
    ]

    indexed_posts = [
        await indexer.get_content_from_links(topics) for topics in indexed_categories
    ]

asyncio.run(main())
