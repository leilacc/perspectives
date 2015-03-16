from bs4 import BeautifulSoup
import json
import logging
import requests

from . import api_keys
from . import helpers
from . import logger
from . import news_interface
from . import news_orgs

logging.basicConfig(filename='%s/guardian.log' % logger.cwd,
                    level=logging.DEBUG,
                    format=logger.fmt, datefmt=logger.datefmt)


class Guardian(news_interface.NewsOrg):
  '''Methods for interacting with the Guardian website/API.'''

  def __repr__(self):
    return news_orgs.GUARDIAN

  def get_article(self, url):
    '''Implementation for getting an article from the Guardian.

    url: A URL in the guardian.com domain.

    Returns: The Article representing the article at that url.
    '''
    try:
      html = helpers.get_content(url)
      if not html:
        return None

      soup = BeautifulSoup(html)
      headline = soup.h1.string.strip('\n')

      if url.split('.com/')[1].startswith('theguardian'):
        article = soup.find('div', attrs={'class': 'flexible-content-body'})
      else:
        article = soup.find('div', attrs={'class': 'content__article-body'})
      paragraphs = article.find_all('p', attrs={'class': None})
      body = ' '.join([p.get_text() for p in paragraphs])

      date = soup.find('time', attrs={'itemprop': 'datePublished'}).contents[0]

      headline = helpers.decode(headline)
      body = helpers.decode(body)
      date = helpers.decode(date)

      logger.log.info('URL: %s' % url)
      logger.log.info('headline: %s' % headline)
      logger.log.info('Body: %s' % body)

      return news_interface.Article(headline, body, url, news_orgs.GUARDIAN,
                                    date)
    except Exception as e:
      logger.log.error("Hit exception getting article for %s: %s" % (url, e))

  def get_query_results(self, query):
    '''Implementation for getting an article from the Guardian.

    query: A URL-encoded string.

    Returns: A list of the top Articles returned by the query search.
    '''
    res = requests.get(
        'http://content.guardianapis.com/search?q=%s&api-key=%s'
        % (query, api_keys.api_keys[news_orgs.GUARDIAN]))
    results = json.loads(res.text)['response']['results']
    article_urls = [res['webUrl'] for res in results]

    top_articles = []
    for url in article_urls[0:news_interface.NUM_ARTICLES]:
      top_articles.append(self.get_article(url))
    return top_articles
