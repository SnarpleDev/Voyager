import grequests as gr
import requests as r
import bs4 as bs
from alive_progress import alive_bar
from helper import convert_et_to_utc, relate
from surrealdb import Surreal


class TopicIndexer:
    def __init__(self, db: Surreal):
        self.db = db

    async def _index_category(self, category: int, page: int = 1):
        result = r.get(
            f"https://scratch.mit.edu/discuss/{category}/?page={page}"
        ).content
        soup = bs.BeautifulSoup(result, "html.parser")
        topics = soup.find_all(attrs={"class": "tclcon"})
        if len(topics) == 0:  # check if forum is empty
            return "No more to crawl"

        data = []

        with alive_bar(len(topics), title=f"Indexing category, page {page}") as bar:
            for topic in topics:
                link: int = topic.find("a")["href"].split("/")[3]  # get topic id
                title: str = topic.find("a").text.strip()  # get topic title
                author: str = (
                    topic.find("span", class_="byuser").text.strip().replace("by ", "")
                )
                is_sticky: bool = (
                    "Sticky:" in topic.get_text()
                    and "Sticky:" not in topic.find("h3").get_text()
                )
                is_closed: int = "closed-topic" in topic.get("class", [])

                to_insert: dict = {
                    "topic_id": int(link),
                    "title": title,
                    "author": author,
                    "sticky": is_sticky,
                    "closed": is_closed,
                }

                result = await self.db.create("Topic", to_insert)

                to_insert["id"] = result[0]["id"]
                data.append(to_insert)

                bar()

        return data

    async def get_content_from_links(self, topics: list, page: int = 1):
        content = {}
        urls = [
            f"https://scratch.mit.edu/discuss/topic/{topic['topic_id']}/?page={page}"
            for topic in topics
        ]

        rs = (gr.get(u) for u in urls)
        with alive_bar(len(topics), title="Fetching content") as bar:
            responses = gr.map(rs)
            for topic, response in zip(topics, responses):
                if response is None:
                    continue

                soup = bs.BeautifulSoup(response.text, "html.parser")

                links = soup.find_all(attrs={"class": "blockpost"})  # find all posts
                content[topic["topic_id"]] = []

                for link_el in links:
                    box = link_el.find("div", attrs={"class": "box"})
                    box_head = box.find("div", attrs={"class": "box-head"})

                    box_content = box.find(
                        "div", attrs={"class": "box-content"}
                    )  # post content

                    post_link = box_head.find("a")["href"].split("/")[3]  # post id

                    post_idx = box_head.find("span").get_text()[
                        1:
                    ]  # post index (represented as #int)

                    post_author = box_content.find("a", attrs={"class": "username"})[
                        "href"
                    ].split("/")[2]  # post author

                    post_content_html = box_content.find(
                        "div", attrs={"class": "post_body_html"}
                    ).decode_contents()  # content as html

                    post_content_bbcode = r.get(
                        f"https://scratch.mit.edu/discuss/post/{int(post_link)}/source"
                    ).content  # content as bbcode

                    post_date = convert_et_to_utc(
                        box_head.find("a").get_text()
                    )  # posting date, in UTC

                    to_insert = {
                        "post_id": int(post_link),
                        "idx": int(post_idx),
                        "author": post_author,
                        "content_html": str(post_content_html),
                        "content_bbcode": bytes(post_content_bbcode).decode(),
                        "date": post_date,
                    }

                    content[topic["topic_id"]].append(to_insert)
                    result = await self.db.create("Post", to_insert)
                    await relate(self.db, topic["id"], result[0]["id"], "posts")
                bar()
        return content
