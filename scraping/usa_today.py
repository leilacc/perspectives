import logging
import requests
import xmltodict

from logger import log
import news_interface
import news_orgs
import api_keys

logging.basicConfig(filename='usa_today.log', level=logging.WARNING)

class USAToday(news_interface.NewsOrg):
  '''Methods for interacting with the USA Today website/API.'''

  def get_article(self, url):
    '''Implementation for getting an article from USA Today.'''
    return 'got it'

  def get_query_results(self, query):
    '''Implementation for keyword searches from USA Today.'''
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
      headline = article['title']
      link = article['link']
      body = self.get_article(link)
      top_articles.append(
          news_interface.Article(headline, body, link, news_orgs.USA_TODAY))
    return top_articles
