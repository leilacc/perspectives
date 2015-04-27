from bs4 import BeautifulSoup

import helpers
import news_interface
import news_orgs


class NYPost(news_interface.NewsOrg):
  '''Methods for interacting with the New York Post website.

  Example usage:
  >>> import new_york_post
  >>> nyp = new_york_post.NewYorkPost()
  >>> nyp.get_article('http://nypost.com/2015/01/25/paris-terrorists-fit-profile-of-homegrown-threat-described-in-2007-nypd-report/')
  '''

  def __init__(self):
    self.news_org = news_orgs.NY_POST
    self.search_url = 'http://nypost.com/?s=%s'

  def __repr__(self):
    return self.news_org

  def get_headline(self, soup):
    headline = soup.h1.a.string
    return headline

  def get_body(self, soup):
    article = soup.find('div', attrs={'class': 'entry-content'})
    paragraphs = article.find_all('p', attrs={'class': None})
    body = ' '.join(
        [helpers.decode(p.get_text()) for p in paragraphs])
    return body

  def get_date(self, soup):
    date = soup.find('p', attrs={'class': 'byline-date'}).string
    return date

  def process_search_results(self, res):
    soup = BeautifulSoup(res.text)
    articles = soup.find_all('article', attrs={'class': 'article'})
    article_urls = [article.h3.a.get('href') for article in articles]
    return article_urls
