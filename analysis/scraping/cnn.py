from bs4 import BeautifulSoup
import logging
import requests
import urllib2

from logger import log
import news_interface
import news_orgs

logging.basicConfig(filename='cnn.log', level=logging.WARNING)

class CNN(news_interface.NewsOrg):
  '''Methods for interacting with the CNN website.'''

  def get_article(self, url):
    '''Implementation for getting an article from CNN.

    Args:
      url: A URL in the www.cnn.* domain.

    Returns:
      The Article representing the article at that url.
    '''
    response = urllib2.urlopen(url)
    html = response.read()
    soup = BeautifulSoup(html)
    a = soup.find("title")
    k = a.text.split("-")
    headline = k[0]
    date = k[1]
    c = soup.findAll("p", attrs={'class': 'zn-body__paragraph'})
    body = ""
    for paragraph in c:
        try:
            body += paragraph.text.decode("utf-8").replace("\"","'") + " "
        except UnicodeEncodeError:
            pass
    log.info(headline)
    log.info(body)
    return news_interface.Article(headline, body, url, news_orgs.CNN)

  def get_query_results(self, query):
    '''Implementation for keyword searches from CNN.

    Args:
      query: A URL-encoded string.

    Returns:
      A list of the top Articles returned by the query search.
    '''
    res = requests.get("http://searchapp.cnn.com/search/query.jsp?page=1&npp=10&start=1&text=%s&type=all&bucket=true&sort=relevance&csiID=csi1" % (query))
    output = res.text.encode('ascii', 'ignore').split("\"url\":")

    article_urls = []
    for line in output:
      try:
        a = line.split(",")[0].replace('"',"")
        if "http" in a:
          article_urls.append(a)
      except:
        pass

    top_articles = []
    for url in article_urls[0:news_interface.NUM_ARTICLES]:
      top_articles.append(self.get_article(url))
    return top_articles
