import api_keys
import news_interface
import news_orgs


class JPost(news_interface.NewsOrg):
  '''Methods for interacting with the JPOST website.'''

  def __init__(self):
    self.news_org = news_orgs.JPOST
    self.search_url = ("https://www.googleapis.com/customsearch/v1?key=" +
        api_keys.api_keys[self.news_org] +
        "&cx=012860551684240964068:7b9pexdovug&q=%s&start=1&callback=getCSERe" +
        "sults")

  def __repr__(self):
    return self.news_org

  def get_headline(self, soup):
    a = soup.find('h1', attrs={'class': 'article-title'})
    headline = a.text.strip().strip('\r\n')
    return headline

  def get_body(self, soup):
    paragraphs = soup.find("div", {"class": "article-text"})
    article = paragraphs.find("p")
    body = article.text
    return body

  def get_date(self, soup):
    date = soup.find('p', attrs={'class': 'article-date-time'}).string
    return date

  def process_search_results(self, res):
    output = res.text.encode('ascii', 'ignore').split("\n")
    article_urls = []
    for line in output:
      if "link" in line and "googleapis" not in line:
        url = line.replace("\"link\": \"","").replace("\"","").strip(",").strip()
        article_urls.append(url)
    return article_urls
