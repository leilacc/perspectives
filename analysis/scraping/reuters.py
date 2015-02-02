from bs4 import BeautifulSoup
import logging
import requests

import helpers
from logger import log
import news_interface
import news_orgs

logging.basicConfig(filename='reuters.log', level=logging.WARNING)

class Reuters(news_interface.NewsOrg):
  '''Methods for interacting with the REUTERS website.'''

  def get_article(self, url):
    '''Implementation for getting an article from REUTERS.

    url: A URL in the www.reuters.com* domain.

    Returns: The Article representing the article at that url.
    '''
    html = helpers.get_content(url)
    if not html:
      return None

    soup = BeautifulSoup(html)
    headline_div = soup.find('div', attrs={'class': 'column1 gridPanel grid8'})
    headline = helpers.decode(headline_div.h1.string)
    paragraphs = soup.find('div', attrs={'class': 'column1 gridPanel grid8'}).findAll("p")
    body = ' '.join([helpers.decode(p.text) for p in paragraphs])
    log.info(headline)
    log.info(body)
    return news_interface.Article(headline, body, url, news_orgs.REUTERS)

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
