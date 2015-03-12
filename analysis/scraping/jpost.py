from bs4 import BeautifulSoup
import logging
import requests

from . import helpers
from . import logger
from . import news_interface
from . import news_orgs

logging.basicConfig(filename='%s/jpost.log' % logger.cwd,
                    level=logging.DEBUG,
                    format=logger.fmt, datefmt=logger.datefmt)


class JPost(news_interface.NewsOrg):
  '''Methods for interacting with the JPOST website.'''

  def __repr__(self):
    return news_orgs.JPOST

  def get_article(self, url):
    '''Implementation for getting an article from JPost.

    Args:
      url: A URL in the www.jpost.com/* domain.

    Returns:
      The Article representing the article at that url.
    '''
    try:
      html = helpers.get_content(url)
      if not html:
        return None

      soup = BeautifulSoup(html)

      try:
        a = soup.find('h1', attrs={'class': 'article-title'})
        headline = a.text.strip().strip('\r\n')
        paragraphs = soup.find("div", {"class": "article-text"})
        article = paragraphs.find("p")
        date = soup.find('p', attrs={'class': 'article-date-time'}).string
      except Exception as e:
        logger.log.error('Error scraping JPost article at %s: %s' % (url, e))

      body = article.text

      headline = helpers.decode(headline)
      body = helpers.decode(body)
      date = helpers.decode(date)

      logger.log.info('URL: %s' % url)
      logger.log.info('headline: %s' % headline)
      logger.log.info('Body: %s' % body)

      return news_interface.Article(headline, body, url, news_orgs.JPOST, date)
    except Exception as e:
      logger.log.error("Hit exception getting article for %s: %s" % (url, e))

  def get_query_results(self, query):
    '''Implementation for keyword searches from JPost.

    Args:
      query: A URL-encoded string.

    Returns:
      A list of the top Articles returned by the query search.
    '''
    res = requests.get("https://www.googleapis.com/customsearch/v1?key=AIzaSyCMGfdDaSfjqv5zYoS0mTJnOT3e9MURWkU&cx=012860551684240964068:7b9pexdovug&q=%s&start=1&callback=getCSEResults" % (query))
    output = res.text.encode('ascii', 'ignore').split("\n")
    article_urls = []
    for line in output:
      if "link" in line and "googleapis" not in line:
        url = line.replace("\"link\": \"","").replace("\"","").strip(",").strip()
        article_urls.append(url)
    top_articles = []
    for url in article_urls[0:news_interface.NUM_ARTICLES]:
      top_articles.append(self.get_article(url))
    return top_articles
