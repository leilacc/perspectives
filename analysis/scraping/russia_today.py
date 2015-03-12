from bs4 import BeautifulSoup
import logging
import requests

from . import helpers
from . import logger
from . import news_interface
from . import news_orgs

logging.basicConfig(filename='%s/russia_today.log' % logger.cwd,
                    level=logging.DEBUG,
                    format=logger.fmt, datefmt=logger.datefmt)


class RussiaToday(news_interface.NewsOrg):
  '''Methods for interacting with the RussiaToday website/API.'''

  def __repr__(self):
    return news_orgs.RUSSIA_TODAY

  def get_article(self, url):
    '''Implementation for getting an article from the Russia Today.

    url: A URL in the russia_today.com domain.

    Returns: The Article representing the article at that url.
    '''
    try:
      html = helpers.get_content(url)
      if not html:
        return None

      soup = BeautifulSoup(html)
      headline = helpers.decode(soup.h1.string)

      article = soup.find('div', attrs={'class': 'cont-wp'})
      paragraphs = article.find_all('p', attrs={'class': None})
      p_text = [helpers.decode(p.get_text()) for p in paragraphs]
      # Get rid of 'Tags' and 'Trends' headers, and 'READ MORE' links
      body = ' '.join([p for p in p_text if not (p.startswith('\nREAD') or
                                        p == 'Tags' or
                                        p == 'Trends')])

      date = soup.find('span', attrs={'class': 'time'}).contents[0]

      headline = helpers.decode(headline)
      body = helpers.decode(body)
      date = helpers.decode(date)
      return news_interface.Article(headline, body, url, news_orgs.RUSSIA_TODAY,
                                    date)
    except Exception as e:
      logger.log.info("Hit exception getting article for %s: %s" % (url, e))

  def get_query_results(self, query):
    '''Implementation for getting an article from Russia Today.

    query: A URL-encoded string.

    Returns: A list of the top Articles returned by the query search.
    '''
    res = requests.get('http://rt.com/search/news/term/%s' % (query))
    soup = BeautifulSoup(res.text)
    query_results = soup.find_all('div', attrs={'class': 'searchtopic'})
    article_urls = ['http://rt.com' + result.a.get('href')
                    for result in query_results]

    top_articles = []
    for url in article_urls[0:news_interface.NUM_ARTICLES]:
      top_articles.append(self.get_article(url))
    return top_articles
