from bs4 import BeautifulSoup
import logging
import requests

from . import helpers
from . import logger
from . import news_interface
from . import news_orgs

logging.basicConfig(filename='%s/todays_zaman.log' % logger.cwd,
                    level=logging.DEBUG,
                    format=logger.fmt, datefmt=logger.datefmt)


class TodaysZaman(news_interface.NewsOrg):
  '''Methods for interacting with the Todays Zaman website.'''

  def __repr__(self):
    return news_orgs.TODAYS_ZAMAN

  def get_article(self, url):
    '''Implementation for getting an article from Todays Zaman.

    Args:
      url: A URL in the www.todayszaman.com/* domain.

    Returns:
      The Article representing the article at that url.
    '''
    try:
      html = helpers.get_content(url)
      if not html:
        return None

      soup = BeautifulSoup(html)
      a = soup.find("title")
      headline = helpers.decode(a.text)
      paragraphs = soup.find("div", {"id": "newsText"})
      article = paragraphs.findAll("p")
      body = ' '.join([helpers.decode(p.text) for p in article])
      dateDiv = soup.find('div', attrs={'class': 'pageNewsDetailDate'})
      date = dateDiv.contents[1].getText()

      headline = helpers.decode(headline)
      body = helpers.decode(body)
      date = helpers.decode(date)

      logger.log.info('URL: %s' % url)
      logger.log.info('headline: %s' % headline)
      logger.log.info('Body: %s' % body)

      return news_interface.Article(headline, body, url, news_orgs.TODAYS_ZAMAN,
                                    date)
    except Exception as e:
      logger.log.error("Hit exception getting article for %s: %s" % (url, e))

  def get_query_results(self, query):
    '''Implementation for keyword searches from Todays Zaman.

    Args:
      query: A URL-encoded string.

    Returns:
      A list of the top Articles returned by the query search.
    '''

    res = requests.get(
      'http://www.todayszaman.com/search.action;jsessionid=bGucr4qN9Lo-TclLpIykGYg1?archiveDate=&words=%s'
      % (query))
    soup = BeautifulSoup(res.text)
    articles = soup.findAll("div", {"class": "pageSearchMainContentText"})

    article_urls = [article.a.get('href') for article in articles]

    top_articles = []
    for url in article_urls[0:news_interface.NUM_ARTICLES]:
      top_articles.append(self.get_article(url))

    return top_articles
