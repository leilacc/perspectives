from bs4 import BeautifulSoup
import logging
import requests

from . import helpers
from . import logger
from . import news_interface
from . import news_orgs

logging.basicConfig(filename='reuters.log', level=logging.WARNING)

class Reuters(news_interface.NewsOrg):
  '''Methods for interacting with the REUTERS website.'''

  def __repr__(self):
    return news_orgs.REUTERS

  def get_article(self, url):
    '''Implementation for getting an article from REUTERS.

    url: A URL in the www.reuters.com* domain.

    Returns: The Article representing the article at that url.
    '''
    try:
      html = helpers.get_content(url)
      if not html:
        return None

      soup = BeautifulSoup(html)
      headline_div = soup.find('div',
                               attrs={'class': 'column1 gridPanel grid8'})
      headline = helpers.decode(headline_div.h1.string)
      body = soup.find('span', attrs={'id': 'articleText'}).getText()
      body = helpers.decode(body)

      date = soup.find('span', attrs={'class': 'timestamp'}).string

      headline = helpers.decode(headline)
      body = helpers.decode(body)
      date = helpers.decode(date)
      return news_interface.Article(headline, body, url, news_orgs.REUTERS,
                                    date)
    except Exception as e:
      logger.log.info("Hit exception getting article for %s: %s" % (url, e))

  def get_query_results(self, query):
    '''Implementation for keyword searches from REUTERS.

    query: A URL-encoded string.

    Returns: A list of the top Articles returned by the query search.
    '''
    res = requests.get('http://www.reuters.com/search?blob=%s' % (query))
    soup = BeautifulSoup(res.text)
    articles = soup.findAll('li', attrs={'class': 'searchHeadline'})
    article_urls = [article.a.get('href') for article in articles]

    top_articles = []
    for url in article_urls[0:news_interface.NUM_ARTICLES]:
        top_articles.append(self.get_article(url))
    return top_articles
