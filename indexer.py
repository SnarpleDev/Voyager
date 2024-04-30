import requests as r
import bs4 as bs # seriously? i've been trying to import beautifulsoup4 and it's imported with bs4??? pure evil

class ForumIndexer:
    def __init__(self, category_list):
        self.category_list = category_list
    
    def _index_category(self, category: int, page: int = 1):
        result = r.get(f"https://scratch.mit.edu/discuss/{category}/?page={page}").content
        soup = bs.BeautifulSoup(result, "html.parser")
        links = []
        t = soup.find_all(attrs={"class": "tclcon"})
        if len(t) == 0:
            return "No more to crawl"
        for el in t:
            link = el.find("a")["href"].split("/")[3]
            links.append(link)
        return [int(link) for link in links]
    
    def get_content_from_links(self, topic_links: list, page: int = 1):
        content = {}
        for link in topic_links:
            result = r.get(f"https://scratch.mit.edu/discuss/topic/{link}/?page={page}").text
            soup = bs.BeautifulSoup(result, "html.parser")
            links = soup.find_all(attrs={"class": "blockpost"})
            # content should be an object with keys called topic_id value link and posts should be a list of links
            content[link] = []
            for link_el in links:
                content[link].append(link_el.find("div", attrs={"class": "box"}).find("div", attrs={"class": "box-head"}).find("a")["href"].split("/")[3])
        return content

indexer = ForumIndexer("asd")
print(indexer._index_category(3))
print(indexer.get_content_from_links(indexer._index_category(1)))