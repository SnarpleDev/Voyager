import asyncio
from surrealdb import Surreal
from indexer import TopicIndexer
from dotenv import load_dotenv
from os import getenv


# This is just temporal, it indexes the first page of Suggestions, and the first page of every topic.
async def main():
    load_dotenv()

    db = Surreal("ws://127.0.0.1:8000/rpc")
    await db.connect()
    await db.use(namespace="Voyager", database="Voyager")
    await db.signin({"user": getenv("USERNAME"), "pass": getenv("PASSWORD")})
    indexer = TopicIndexer(db)
    indexed = await indexer._index_category(1)
    await indexer.get_content_from_links(indexed)
    print("Successfully indexed!")


asyncio.run(main())
