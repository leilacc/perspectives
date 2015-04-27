from bs4 import BeautifulSoup

import news_interface
import news_orgs


class CNN(news_interface.NewsOrg):
  '''Methods for interacting with the CNN website.'''

  def __init__(self):
    self.news_org = news_orgs.CNN
    self.search_url = "http://searchapp.cnn.com/search/query.jsp?page=1&npp=10&start=1&text=%s&type=all&bucket=true&sort=relevance&csiID=csi1"

  def __repr__(self):
    return self.news_org

  def get_headline(self, soup):
    a = soup.find("title")
    k = a.text.split("-")
    headline = k[0]
    return headline

  def get_body(self, soup):
    c = soup.findAll("p", attrs={'class': 'zn-body__paragraph'})
    body = ""
    for paragraph in c:
        try:
            body += paragraph.text.decode("utf-8").replace("\"","'") + " "
        except UnicodeEncodeError:
            pass
    return body

  def get_date(self, soup):
    try:
      date = soup.find('p', attrs={'class': 'update-time'}).string
    except AttributeError:
      date = soup.find('p', attrs={'class': 'metadata__data-added'}).string
    return date

  def process_search_results(self, res):
    output = res.text.encode('ascii', 'ignore').split("\"url\":")

    article_urls = []
    for line in output:
      try:
        a = line.split(",")[0].replace('"',"")
        if "http" in a:
          article_urls.append(a)
      except:
        pass
    return article_urls
