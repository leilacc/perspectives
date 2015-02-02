from bs4 import BeautifulSoup
import logging
import requests

import helpers
from logger import log
import news_interface
import news_orgs

import urllib2


logging.basicConfig(filename='todays_zaman.log', level=logging.WARNING)

class TodaysZaman(news_interface.NewsOrg):
  '''Methods for interacting with the Todays Zaman website.'''

  def get_article(self, url):
    '''Implementation for getting an article from Todays Zaman.

    Args:
      url: A URL in the www.todayszaman.com/* domain.

    Returns:
      The Article representing the article at that url.
    '''
    html = helpers.get_content(url)
    if not html:
      return None

    soup = BeautifulSoup(html)
    a = soup.find("title")
    headline = helpers.decode(a.text)
    paragraphs = soup.find("div", {"id": "newsText"})
    article = paragraphs.findAll("p")
    body = ' '.join([helpers.decode(p.text) for p in article])
    log.info(headline)
    log.info(body)
    return news_interface.Article(headline, body, url, news_orgs.TODAYS_ZAMAN)

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

