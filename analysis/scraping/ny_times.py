from bs4 import BeautifulSoup
import json
import logging
import requests

from . import api_keys
from . import helpers
from . import logger
from . import news_interface
from . import news_orgs

logging.basicConfig(filename='%s/ny_times.log' % logger.cwd,
                    level=logging.DEBUG,
                    format=logger.fmt, datefmt=logger.datefmt)


class NYTimes(news_interface.NewsOrg):
  '''Methods for interacting with the NYTimes website/API.'''

  def __repr__(self):
    return news_orgs.NY_TIMES

  def get_article(self, url):
    '''Implementation for getting an article from the NYTimes.

    url: A URL in the ny_times.com domain.

    Returns: The Article representing the article at that url.
    '''
    try:
      html = helpers.get_content(url)
      if not html:
        return None

      soup = BeautifulSoup(html)
      headline = helpers.decode(soup.h1.string)

      try:
        article = soup.find('div', attrs={'class': 'articleBody'})
        paragraphs = article.find_all('p', attrs={'itemprop': 'articleBody'})
      except AttributeError:
        # this article's html uses different attributes... sigh...
        # Hopefully there are only 2 versions
        article = soup.find('div', attrs={'class': 'story-body'})
        paragraphs = article.find_all('p', attrs={'class': 'story-content'})

      p_text = [helpers.decode(p.get_text()) for p in paragraphs]
      body = ' '.join([p for p in p_text])

      try:
        date = soup.find('h6', attrs={'class': 'dateline'}).string
      except AttributeError:
        date = soup.find('time', attrs={'class': 'dateline'}).string

      headline = helpers.decode(headline)
      body = helpers.decode(body)
      date = helpers.decode(date)

      logger.log.info('URL: %s' % url)
      logger.log.info('headline: %s' % headline)
      logger.log.info('Body: %s' % body)

      return news_interface.Article(headline, body, url, news_orgs.NY_TIMES,
                                    date)
    except Exception as e:
      logger.log.error("Hit exception getting article for %s: %s" % (url, e))

  def get_query_results(self, query):
    '''Implementation for getting an article from NYTimes.

    query: A URL-encoded string.

    Returns: A list of the top Articles returned by the query search.
    '''
    res = requests.get(
        'http://api.nytimes.com/svc/search/v2/articlesearch.json?q=%s&api-key=%s'
        % (query, api_keys.api_keys[news_orgs.NY_TIMES]))
    results = json.loads(res.text)['response']['docs']
    # web_urls have this weird '\/' instead of '/' for some reason
    article_urls = [res['web_url'].replace('\/', '/') for res in results]

    top_articles = []
    for url in article_urls[0:news_interface.NUM_ARTICLES]:
      top_articles.append(self.get_article(url))
    return top_articles
