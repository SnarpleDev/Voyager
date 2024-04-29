import requests as r
import beautifulsoup4 as bs

class ForumIndexer:
    def __init__(self, category_list):
        self.category_list = category_list
    
    def _index_category(self, category, page=1):
        result = r.get(f"https://scratch.mit.edu/discuss/{category}/?page={page}").content
        soup = bs.BeautifulSoup(result, "html.parser")
        links = []
        t = soup.find_all(attrs={"class": "tclcon"})
        if len(t) == 0:
            return "No more to crawl"
        for el in t:
            link = el.find("a")["href"]
            links.append(link)
        return links