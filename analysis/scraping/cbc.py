from bs4 import BeautifulSoup

import logger
import news_interface
import news_orgs


class CBC(news_interface.NewsOrg):
  '''Methods for interacting with the CBC website.'''

  def __init__(self):
    self.news_org = news_orgs.CBC
    self.search_url = 'http://search.cbc.ca/search?site=2011-News&output=xml_no_dtd&ie=utf8&oe=utf8&safe=high&getfields=*&client=cbc-global&proxystylesheet=cbc-global&proxyreload=1&q=%s'

  def __repr__(self):
    return self.news_org

  def get_headline(self, soup):
    try:
      headline = soup.h1.string
    except AttributeError:
      logger.log.error('Exception trying to scrape CBC headline from %s'
                % (url))
      return None
    return headline

  def get_body(self, soup):
    article = soup.find('div', attrs={'class': 'story-content'})
    paragraphs = article.find_all('p', attrs={'class': None})
    body = ' '.join([p.get_text() for p in paragraphs])
    return body

  def get_date(self, soup):
    date = soup.find('span', attrs={'class': 'delimited'}).string
    return date

  def process_search_results(self, raw_results):
    soup = BeautifulSoup(raw_results.text)
    articles = soup.find_all('p', attrs={'class': 'g'})
    article_urls = [article.a.get('href') for article in articles]
    return article_urls
