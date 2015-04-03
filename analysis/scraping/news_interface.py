from bs4 import BeautifulSoup
import logging
import requests
import sys

import helpers
import logger
import news_interface
import news_orgs

NUM_ARTICLES = 2

logging.basicConfig(filename='%s/scraping.log' % logger.cwd,
                    level=logging.DEBUG,
                    format=logger.fmt, datefmt=logger.datefmt)


def _functionId(obj, nFramesUp):
    '''Create a string naming the function n frames up on the stack.'''
    fr = sys._getframe(nFramesUp+1)
    co = fr.f_code
    return "%s.%s" % (obj.__class__, co.co_name)

def abstractMethod(obj=None):
    '''Use this instead of 'pass' for the body of abstract methods.'''
    raise Exception("Unimplemented abstract method: %s" % _functionId(obj, 1))


class NewsOrg:
  '''Represents a news organization.'''

  def __repr__(self):
    '''Representation of the NewsOrg.'''
    abstractMethod(self)

  def get_headline(self, soup):
    '''Returns an article's headline given the soupified article.'''
    abstractMethod(self)

  def get_body(self, soup):
    '''Returns an article's body given the soupified article.'''
    abstractMethod(self)

  def get_date(self, soup):
    '''Returns an article's date given the soupified article.'''
    abstractMethod(self)

  def get_article(self, url):
    '''Returns an Article representing the article at url.'''
    try:
      html = helpers.get_content(url)
      if not html:
        return None

      soup = BeautifulSoup(html)
      headline = self.get_headline(soup)
      body = self.get_body(soup)
      date = self.get_date(soup)
    except Exception as e:
      logger.log.error("Hit exception on line number %s getting article for %s:"
                       " %s" % (sys.exc_info()[-1].tb_lineno, url, e))
      return None

    try:
      headline = helpers.decode(headline)
      body = helpers.decode(body)
      date = helpers.decode(date)
    except Exception as e:
      logger.log.error('Error on line %s decoding url %s: %s' %
                       (sys.exc_info()[-1].tb_lineno, url, e))
      return None

    logger.log.info('URL: %s' % url)
    logger.log.info('headline: %s' % headline)
    logger.log.info('Body: %s' % body)

    return news_interface.Article(headline, body, url, self.news_org,
                                  date)

  def get_raw_search_results(self, query):
    '''Returns the raw search results for a given query.'''
    abstractMethod(self)

  def process_search_results(self, results):
    '''Returns a list of search result urls given the raw results.'''
    abstractMethod(self)

  def get_query_results(self, query):
    '''Return a list of NUM_ARTICLES Articles returned by query.

    Args:
      query: A URL-encoded string.

    Returns:
      A list of the top Articles returned by the query search.
    '''
    try:
      search_results = requests.get(self.search_url % (query),
                                    timeout=helpers.TIMEOUT)
    except requests.exceptions.Timeout as e:
      logger.log.error('Requests timeout for %s in get_query_results: %s' %
                       (self, e))
      return None

    result_urls = self.process_search_results(search_results)
    top_articles = []
    for url in result_urls[0:news_interface.NUM_ARTICLES]:
      top_articles.append(self.get_article(url))
    return top_articles


class Article:
  '''Represents an article.'''

  def __init__(self, headline, body, link, news_org, date):
    '''Initialize the article's properties.

    headline: str
    body: str
    link: str
    news_org: str. See the macros in api_keys
    date: str, unaltered from scraping
    '''
    self.headline = headline
    self.body = body
    self.link = link
    self.news_org = news_org
    self.date = date

  def __repr__(self):
    '''Representation of the article.'''
    return ('----------------------------------------------------------------\n'
            'ARTICLE\n'
            'Org: %s\n'
            'Headline: %s...\n'
            'Date: %s\n'
            'Body: %s...\n'
            'Link: %s\n'
            % (self.news_org, self.headline[0:66], self.date,
               self.body[0:70], self.link))

  def to_dict(self):
    '''Return the Article represented in dictionary form.

    article: an Article

    Returns: A dictionary representation of the article.
    '''
    article_dict = {}
    article_dict["headline"] = self.headline
    article_dict["body"] = self.body
    article_dict["link"] = self.link
    article_dict["news_org"] = self.news_org
    article_dict["date"] = self.date
    return article_dict
