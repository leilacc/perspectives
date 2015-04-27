from bs4 import BeautifulSoup

from . import helpers
from . import news_interface
from . import news_orgs


class TodaysZaman(news_interface.NewsOrg):
  '''Methods for interacting with the Todays Zaman website.'''

  def __init__(self):
    self.news_org = news_orgs.TODAYS_ZAMAN
    self.search_url = 'http://www.todayszaman.com/search.action;jsessionid=bGucr4qN9Lo-TclLpIykGYg1?archiveDate=&words=%s'

  def __repr__(self):
    return self.news_org

  def get_headline(self, soup):
    headline = soup.find("title").text
    return headline

  def get_body(self, soup):
    paragraphs = soup.find("div", {"id": "newsText"})
    article = paragraphs.findAll("p")
    body = ' '.join([helpers.decode(p.text) for p in article])
    return body

  def get_date(self, soup):
    dateDiv = soup.find('div', attrs={'class': 'pageNewsDetailDate'})
    date = dateDiv.contents[1].getText()
    return date

  def process_search_results(self, res):
    soup = BeautifulSoup(res.text)
    articles = soup.findAll("div", {"class": "pageSearchMainContentText"})

    article_urls = [article.a.get('href') for article in articles]
    return article_urls
