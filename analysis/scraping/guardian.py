from bs4 import BeautifulSoup
import json

import api_keys
import news_interface
import news_orgs


class Guardian(news_interface.NewsOrg):
  '''Methods for interacting with the Guardian website/API.'''

  def __init__(self):
    self.news_org = news_orgs.GUARDIAN
    self.search_url = ('http://content.guardianapis.com/search?q=%s&api-key=' +
                       api_keys.api_keys[news_orgs.GUARDIAN])

  def __repr__(self):
    return self.news_org

  def get_headline(self, soup):
    headline = soup.h1.string.strip('\n')
    return headline

  def get_body(self, soup):
    article = soup.find('div', attrs={'class': 'flexible-content-body'})
    if not article:
      article = soup.find('div', attrs={'class': 'content__article-body'})
    paragraphs = article.find_all('p', attrs={'class': None})
    body = ' '.join([p.get_text() for p in paragraphs])
    return body

  def get_date(self, soup):
    date = soup.find('time', attrs={'itemprop': 'datePublished'}).contents[0]
    return date

  def process_search_results(self, res):
    results = json.loads(res.text)['response']['results']
    article_urls = [res['webUrl'] for res in results]
    return article_urls
