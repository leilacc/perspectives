from bs4 import BeautifulSoup

import news_interface
import news_orgs


class BBC(news_interface.NewsOrg):
  '''Methods for interacting with the BBC website.'''

  def __init__(self):
    self.news_org = news_orgs.BBC
    self.search_url = 'http://www.bbc.co.uk/search?q=%s&sa_f=search-serp&filter=news'

  def __repr__(self):
    return self.news_org

  def get_headline(self, soup):
    headline = soup.h1.string
    return headline

  def get_body(self, soup):
    article = soup.find('div', attrs={'class': 'story-body'})
    paragraphs = article.find_all('p', attrs={'class': None})
    body = ' '.join([p.get_text() for p in paragraphs])
    return body

  def get_date(self, soup):
    date = soup.find('span', attrs={'class': 'date'}).string
    return date

  def process_search_results(self, res):
    soup = BeautifulSoup(res.text)
    articles = soup.find_all('article')
    article_urls = [article.h1.a.get('href') for article in articles]
    return article_urls
