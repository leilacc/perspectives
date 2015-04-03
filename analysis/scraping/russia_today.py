from bs4 import BeautifulSoup

import helpers
import news_interface
import news_orgs


class RussiaToday(news_interface.NewsOrg):
  '''Methods for interacting with the RussiaToday website/API.'''

  def __init__(self):
    self.news_org = news_orgs.RUSSIA_TODAY
    self.search_url = 'http://rt.com/search/news/term/%s'

  def __repr__(self):
    return self.news_org

  def get_headline(self, soup):
    headline = soup.h1.string
    return headline

  def get_body(self, soup):
    article = soup.find('div', attrs={'class': 'cont-wp'})
    paragraphs = article.find_all('p', attrs={'class': None})
    p_text = [helpers.decode(p.get_text()) for p in paragraphs]
    # Get rid of 'Tags' and 'Trends' headers, and 'READ MORE' links
    body = ' '.join([p for p in p_text if not (p.startswith('\nREAD') or
                                      p == 'Tags' or
                                      p == 'Trends')])
    return body

  def get_date(self, soup):
    date = soup.find('span', attrs={'class': 'time'}).contents[0]
    return date

  def process_search_results(self, res):
    soup = BeautifulSoup(res.text)
    query_results = soup.find_all('div', attrs={'class': 'searchtopic'})
    article_urls = ['http://rt.com' + result.a.get('href')
                    for result in query_results]
    return article_urls
