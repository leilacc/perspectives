from bs4 import BeautifulSoup
import json
import logging
import requests

from api_keys import api_keys
import helpers
from logger import log
import news_interface
import news_orgs

logging.basicConfig(filename='bbc.log', level=logging.WARNING)

class BBC(news_interface.NewsOrg):
  '''Methods for interacting with the BBC website.'''

  def get_article(self, url):
    '''Implementation for getting an article from BBC.

    url: A URL in the www.bbc.* domain.

    Returns: The Article representing the article at that url.
    '''
    html = helpers.get_content(url)
    if not html:
      return None

    soup = BeautifulSoup(html)
    headline = soup.h1.string
    article = soup.find('div', attrs={'class': 'story-body'})
    paragraphs = article.find_all('p', attrs={'class': None})
    body = ' '.join([p.get_text() for p in paragraphs])
    log.info(headline)
    log.info(body)
    return news_interface.Article(headline, body, url, news_orgs.BBC)

  def get_query_results(self, query):
    '''Implementation for keyword searches from BBC.

    query: A URL-encoded string.

    Returns: A list of the top Articles returned by the query search.
    '''
    res = requests.get(
        'http://www.bbc.co.uk/search?q=%s&sa_f=search-serp&filter=news'
        % (query))
    soup = BeautifulSoup(res.text)
    articles = soup.find_all('article')
    article_urls = [article.h1.a.get('href') for article in articles]

    top_articles = []
    for url in article_urls[0:news_interface.NUM_ARTICLES]:
        top_articles.append(self.get_article(url))
    return top_articles
