import requests as r
import bs4 as bs
from alive_progress import alive_bar
class ForumIndexer:
    def __init__(self, category_list):
        self.category_list = category_list
    
    def _index_category(self, category: int, page: int = 1):
        result = r.get(f"https://scratch.mit.edu/discuss/{category}/?page={page}").content
        soup = bs.BeautifulSoup(result, "html.parser")
        topics = soup.find_all(attrs={"class": "tclcon"})
        if len(topics) == 0:
            return "No more to crawl"
        
        data = []
        
        with alive_bar(len(topics), title="Indexing category") as bar:
            for topic in topics:
                link = topic.find("a")["href"].split("/")[3]
                title = topic.find("a").text.strip()
                author = topic.find("span", class_="byuser").text.strip().replace('by ', '')
                is_sticky = "Sticky:" in topic.get_text() and "Sticky:" not in topic.find('h3').get_text()
                is_closed = "closed-topic" in topic.get("class", [])
                
                data.append({
                    "link": int(link),
                    "title": title,
                    "author": author,
                    "sticky": is_sticky,
                    "closed": is_closed
                })
                bar()
        
        return data
    
    def get_content_from_links(self, topics: list, page: int = 1):
        content = {}
        with alive_bar(len(topics), title="Fetching content") as bar:
            for topic in topics:
                result = r.get(f"https://scratch.mit.edu/discuss/topic/{topic["link"]}/?page={page}").text
                soup = bs.BeautifulSoup(result, "html.parser")
                links = soup.find_all(attrs={"class": "blockpost"})
                content[topic["link"]] = []
                for link_el in links:
                    post_link = link_el.find("div", attrs={"class": "box"}).find("div", attrs={"class": "box-head"}).find("a")["href"].split("/")[3]
                    content[topic["link"]].append(int(post_link))
                bar()
        return content

indexer = ForumIndexer("asd")
indexed = indexer._index_category(31)
print(indexer.get_content_from_links(indexed))
