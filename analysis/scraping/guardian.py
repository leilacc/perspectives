from bs4 import BeautifulSoup
import json

import api_keys
import news_interface
import news_orgs


class Guardian(news_interface.NewsOrg):
  '''Methods for interacting with the Guardian website/API.'''

  def __init__(self):
    self.news_org = news_orgs.GUARDIAN
    self.search_url = ('http://www.google.com/cse?oe=utf8&ie=utf8&source=uds&'
                       'q=%s&start=0&sort=&'
                       'cx=007466294097402385199:m2ealvuxh1i')

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
    soup = BeautifulSoup(res.text)
    all_as = soup.find_all('a', attrs={'class': 'l'})
    article_urls = [a.get('href') for a in all_as]
    return article_urls
