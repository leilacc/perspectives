from bs4 import BeautifulSoup
import logging
import requests
import urllib2

import helpers
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
    try:
      html = helpers.get_content(url)
      if not html:
        return None

      soup = BeautifulSoup(html)
      a = soup.find("title")
      k = a.text.split("-")
      headline = helpers.decode(k[0])
      c = soup.findAll("p", attrs={'class': 'zn-body__paragraph'})
      body = ""
      for paragraph in c:
          try:
              body += paragraph.text.decode("utf-8").replace("\"","'") + " "
          except UnicodeEncodeError:
              pass

      try:
        date = soup.find('p', attrs={'class': 'update-time'}).string
      except AttributeError:
        date = soup.find('p', attrs={'class': 'metadata__data-added'}).string

      return news_interface.Article(headline, body, url, news_orgs.CNN, date)
    except Exception as e:
      log.info("Hit exception getting article for %s: %s" % (url, e))

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
