import requests
import xmltodict

import news_interface
import news_orgs
import api_keys


class USAToday(news_interface.NewsOrg):
  '''Methods for interacting with the USA Today website/API.'''

  def get_article(self, url):
    '''Implementation for getting an article from USA Today.'''
    return 'got it'

  def get_query_results(self, query):
    '''Implementation for getting an article from USA Today.'''
    res = requests.post(
        "http://api.usatoday.com/open/articles?keyword=%s&api_key=%s"
        % (query, api_keys.api_keys[news_orgs.USA_TODAY]))
    print res.text
    xml_dict = xmltodict.parse(res.text)
    all_articles = xml_dict['rss']['channel']['item']
    top_articles = []
    for article in all_articles[0:NUM_ARTICLES]:
      headline = article['title']
      link = article['link']
      body = self.get_article(link)
      top_articles.append(Article(headline, body, link, USA_TODAY))
    return top_articles
