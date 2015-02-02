from bs4 import BeautifulSoup
import json
import logging
import requests

from api_keys import api_keys
import helpers
from logger import log
import news_interface
import news_orgs

logging.basicConfig(filename='ny_times.log', level=logging.WARNING)


class NYTimes(news_interface.NewsOrg):
  '''Methods for interacting with the NYTimes website/API.'''

  def get_article(self, url):
    '''Implementation for getting an article from the NYTimes.

    url: A URL in the ny_times.com domain.

    Returns: The Article representing the article at that url.
    '''
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

    log.info(headline)
    log.info(body)
    return news_interface.Article(headline, body, url, news_orgs.NY_TIMES)

  def get_query_results(self, query):
    '''Implementation for getting an article from NYTimes.

    query: A URL-encoded string.

    Returns: A list of the top Articles returned by the query search.
    '''
    res = requests.get(
        'http://api.nytimes.com/svc/search/v2/articlesearch.json?q=%s&api-key=%s'
        % (query, api_keys[news_orgs.NY_TIMES]))
    results = json.loads(res.text)['response']['docs']
    # web_urls have this weird '\/' instead of '/' for some reason
    article_urls = [res['web_url'].replace('\/', '/') for res in results]

    top_articles = []
    for url in article_urls[0:news_interface.NUM_ARTICLES]:
      log.info(url)
      top_articles.append(self.get_article(url))
    return top_articles
