from bs4 import BeautifulSoup
import json
import logging
import requests

import helpers
from logger import log
import news_interface
import news_orgs
import api_keys

logging.basicConfig(filename='cbc.log', level=logging.WARNING)


class CBC(news_interface.NewsOrg):
  '''Methods for interacting with the CBC website.'''

  def get_article(self, url):
    '''Implementation for getting an article from the CBC.

    url: A URL in the cbc.ca/news/* domain.

    Returns: The Article representing the article at that url, or None if
    unable to scrape the article.
    '''
    html = helpers.get_content(url)
    if not html:
      return None

    soup = BeautifulSoup(html)

    try:
      headline = soup.h1.string
    except AttributeError:
      log.error('Exception trying to scrape CBC headline from %s'
                % (url))
      return None

    article = soup.find('div', attrs={'class': 'story-content'})
    paragraphs = article.find_all('p', attrs={'class': None})
    body = ' '.join([p.get_text() for p in paragraphs])
    log.info(headline)
    log.info(body)

    date = soup.find('span', attrs={'class': 'delimited'}).string
    return news_interface.Article(headline, body, url, news_orgs.CBC, date)

  def get_query_results(self, query):
    '''Implementation for getting an article from the CBC.

    query: A URL-encoded string.

    Returns: A list of the top Articles returned by the query search.
    '''
    res = requests.get(
        'http://search.cbc.ca/search?site=2011-News&output=xml_no_dtd&ie=utf8&oe=utf8&safe=high&getfields=*&client=cbc-global&proxystylesheet=cbc-global&proxyreload=1&q=%s'
        % (query))
    soup = BeautifulSoup(res.text)
    articles = soup.find_all('p', attrs={'class': 'g'})
    article_urls = [article.a.get('href') for article in articles]

    top_articles = []
    for url in article_urls[0:news_interface.NUM_ARTICLES]:
        top_articles.append(self.get_article(url))
    return top_articles
