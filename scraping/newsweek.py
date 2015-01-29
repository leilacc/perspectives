from bs4 import BeautifulSoup
import json
import logging
import requests

from api_keys import api_keys
from logger import log
import news_interface
import news_orgs

logging.basicConfig(filename='newsweek.log', level=logging.WARNING)

class NEWSWEEK(news_interface.NewsOrg):
  '''Methods for interacting with the BBC website.'''

  def get_article(self, url):
    '''Implementation for getting an article from Newsweek.

    url: A URL in the www.newsweek.* domain.

    Returns: The Article representing the article at that url.
    '''

    soup = BeautifulSoup(requests.get(url).text)
    headline = soup.find('h1', attrs={'class': 'article-title'}).get_text()
    article = soup.find('div', attrs={'class': 'article-body'})
    paragraphs = article.find_all('p', attrs={'dir': 'ltr'})
    body = ' '.join([p.get_text() for p in paragraphs])
    log.info(headline)
    log.info(body)
    return news_interface.Article(headline, body, url, news_orgs.NEWSWEEK)






  def get_query_results(self, query):
    '''Implementation for keyword searches from Newsweek.

    query: A URL-encoded string.

    Returns: A list of the top Articles returned by the query search.
    '''
    res = requests.get(
        'http://www.newsweek.com/search/site/%s'
        % (query))
    soup = BeautifulSoup(res.text)

    search_results = soup.find_all('li', attrs={'class': 'search-result'})
    article_urls = [result.a.get('href') for result in search_results]

    top_articles = []
    for url in article_urls[0:news_interface.NUM_ARTICLES]:
        top_articles.append(self.get_article(url))
    return top_articles
