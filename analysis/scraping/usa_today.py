from bs4 import BeautifulSoup
import logging
import requests
import xmltodict

import helpers
from logger import log
import news_interface
import news_orgs
import api_keys

logging.basicConfig(filename='usa_today.log', level=logging.WARNING)

class USAToday(news_interface.NewsOrg):
  '''Methods for interacting with the USA Today website/API.'''

  def get_article(self, url):
    '''Implementation for getting an article from USA Today.

    url: A URL in the http://www.usatoday.com/story/* domain.

    Returns: The Article representing the article at that url.
    '''
    try:
      html = helpers.get_content(url)
      if not html:
        return None

      soup = BeautifulSoup(html)
      article = soup.article
      headline = helpers.decode(article.h1.string)
      paragraphs = article.find_all('p', attrs={'class': None})
      body = ' '.join([helpers.decode(p.get_text()) for p in paragraphs])
      time_span = soup.find('span', attrs={'class': 'asset-metabar-time'})
      date = time_span.contents[0]
      return news_interface.Article(headline, body, url, news_orgs.USA_TODAY,
                                    date)
    except Exception as e:
      log.info("Hit exception getting article for %s: %s" % (url, e))

  def get_query_results(self, query):
    '''Implementation for keyword searches from USA Today.

    query: A URL-encoded string.

    Returns: A list of the top Articles returned by the query search.
    '''
    res = requests.get(
        "http://api.usatoday.com/open/articles?keyword=%s&api_key=%s"
        % (query, api_keys.api_keys[news_orgs.USA_TODAY]))
    xml_dict = xmltodict.parse(res.text)

    try:
      all_articles = xml_dict['rss']['channel']['item']
    except KeyError:
      log.error(res.text)

    top_articles = []
    for article in all_articles[0:news_interface.NUM_ARTICLES]:
      link = article['link']
      top_articles.append(self.get_article(link))
    return top_articles
