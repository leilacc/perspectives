from bs4 import BeautifulSoup

import news_interface
import news_orgs


class Reuters(news_interface.NewsOrg):
  '''Methods for interacting with the REUTERS website.'''

  def __init__(self):
    self.news_org = news_orgs.REUTERS
    self.search_url = 'http://www.reuters.com/search?blob=%s'

  def __repr__(self):
    return self.news_org

  def get_headline(self, soup):
    headline_div = soup.find('div',
                             attrs={'class': 'column1 gridPanel grid8'})
    headline = headline_div.h1.string
    return headline

  def get_body(self, soup):
    body = soup.find('span', attrs={'id': 'articleText'}).getText()
    return body

  def get_date(self, soup):
    date = soup.find('span', attrs={'class': 'timestamp'}).string
    return date

  def process_search_results(self, res):
    soup = BeautifulSoup(res.text)
    articles = soup.findAll('li', attrs={'class': 'searchHeadline'})
    article_urls = [article.a.get('href') for article in articles]
    return article_urls
