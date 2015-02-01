from bs4 import BeautifulSoup
import logging
import requests

from api_keys import api_keys
from logger import log
import news_interface
import news_orgs

logging.basicConfig(filename='russia_today.log', level=logging.WARNING)


class RussiaToday(news_interface.NewsOrg):
  '''Methods for interacting with the RussiaToday website/API.'''

  def get_article(self, url):
    '''Implementation for getting an article from the Russia Today.

    url: A URL in the russia_today.com domain.

    Returns: The Article representing the article at that url.
    '''
    # Encoding is off; re-encoding as ascii fixes most of it
    soup = BeautifulSoup(requests.get(url).text.encode('ascii', 'ignore'))
    headline = soup.h1.string

    article = soup.find('div', attrs={'class': 'cont-wp'})
    paragraphs = article.find_all('p', attrs={'class': None})
    p_text = [p.get_text() for p in paragraphs]
    # Get rid of 'Tags' and 'Trends' headers, and 'READ MORE' links
    body = ' '.join([p for p in p_text if not (p.startswith('\nREAD') or
                                      p == 'Tags' or
                                      p == 'Trends')])

    log.info(headline)
    log.info(body)
    return news_interface.Article(headline, body, url, news_orgs.RUSSIA_TODAY)

  def get_query_results(self, query):
    '''Implementation for getting an article from Russia Today.

    query: A URL-encoded string.

    Returns: A list of the top Articles returned by the query search.
    '''
    res = requests.get('http://rt.com/search/news/term/%s' % (query))
    soup = BeautifulSoup(res.text)
    query_results = soup.find_all('div', attrs={'class': 'searchtopic'})
    article_urls = ['http://rt.com' + result.a.get('href')
                    for result in query_results]

    top_articles = []
    for url in article_urls[0:news_interface.NUM_ARTICLES]:
      log.info(url)
      top_articles.append(self.get_article(url))
    return top_articles
