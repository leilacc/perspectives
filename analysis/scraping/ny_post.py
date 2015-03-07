from bs4 import BeautifulSoup
import json
import logging
import requests

import helpers
from logger import log
import news_interface
import news_orgs
import api_keys

logging.basicConfig(filename='ny_post.log', level=logging.WARNING)


class NYPost(news_interface.NewsOrg):
  '''Methods for interacting with the New York Post website.

  Example usage:
  >>> import new_york_post
  >>> nyp = new_york_post.NewYorkPost()
  >>> nyp.get_article('http://nypost.com/2015/01/25/paris-terrorists-fit-profile-of-homegrown-threat-described-in-2007-nypd-report/')
  '''

  def get_article(self, url):
    '''Implementation for getting an article from the New York Post.

    url: A URL in the nypost.com domain.

    Returns: The Article representing the article at that url.
    '''
    try:
      html = helpers.get_content(url)
      if not html:
        return None

      soup = BeautifulSoup(html)
      headline = helpers.decode(soup.h1.a.string)
      article = soup.find('div', attrs={'class': 'entry-content'})
      paragraphs = article.find_all('p', attrs={'class': None})
      body = ' '.join(
          [helpers.decode(p.get_text()) for p in paragraphs])
      date = soup.find('p', attrs={'class': 'byline-date'}).string

      headline = helpers.decode(headline)
      body = helpers.decode(body)
      date = helpers.decode(date)
      return news_interface.Article(headline, body, url, news_orgs.NY_POST,
                                    date)
    except Exception as e:
      log.info("Hit exception getting article for %s: %s" % (url, e))

  def get_query_results(self, query):
    '''Implementation for getting an article from the New York Post.

    query: A URL-encoded string.

    Returns: A list of the top Articles returned by the query search.
    '''
    res = requests.get('http://nypost.com/?s=%s' % (query))
    soup = BeautifulSoup(res.text)
    articles = soup.find_all('article')
    article_urls = [article.h3.a.get('href') for article in articles]

    top_articles = []
    for url in article_urls[0:news_interface.NUM_ARTICLES]:
        top_articles.append(self.get_article(url))
    return top_articles
