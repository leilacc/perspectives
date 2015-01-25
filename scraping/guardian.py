from bs4 import BeautifulSoup
import json
import logging
import requests

from api_keys import api_keys
from logger import log
import news_interface
import news_orgs

logging.basicConfig(filename='guardian.log', level=logging.WARNING)


class Guardian(news_interface.NewsOrg):
  '''Methods for interacting with the Guardian website.'''

  def get_article(self, url):
    '''Implementation for getting an article from the Guardian.

    url: A URL in the guardian.com domain.

    Returns: The Article representing the article at that url.
    '''
    soup = BeautifulSoup(requests.get(url).text)
    headline = soup.h1.string

    if url.split('.com/')[1].startswith('theguardian'):
      article = soup.find('div', attrs={'class': 'flexible-content-body'})
    else:
      article = soup.find('div', attrs={'class': 'content__article-body'})
    paragraphs = article.find_all('p', attrs={'class': None})
    body = ' '.join([p.get_text() for p in paragraphs])

    log.info(headline)
    log.info(body)
    return news_interface.Article(headline, body, url, news_orgs.GUARDIAN)

  def get_query_results(self, query):
    '''Implementation for getting an article from the Guardian.

    query: A URL-encoded string.

    Returns: A list of the top Articles returned by the query search.
    '''
    res = requests.get(
        'http://content.guardianapis.com/search?q=%s&api-key=%s'
        % (query, api_keys[news_orgs.GUARDIAN]))
    results = json.loads(res.text)['response']['results']
    article_urls = [res['webUrl'] for res in results]

    top_articles = []
    for url in article_urls[0:news_interface.NUM_ARTICLES]:
      log.info(url)
      top_articles.append(self.get_article(url))
    return top_articles
