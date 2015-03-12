from bs4 import BeautifulSoup
import json
import logging
import requests

from . import helpers
from . import logger
from . import news_interface
from . import news_orgs

logging.basicConfig(filename='%s/aljazeera.log' % logger.cwd,
                    level=logging.DEBUG,
                    format=logger.fmt, datefmt=logger.datefmt)


class AlJazeera(news_interface.NewsOrg):
  '''Methods for interacting with the Al Jazeera website.'''

  def __repr__(self):
    return news_orgs.ALJAZEERA

  def get_article(self, url):
    '''Implementation for getting an article from Al Jazeera.

    Args:
      url: A URL in the aljazeera.* domain.

    Returns:
      The Article representing the article at that url, or None if unable to
      get the Article.
    '''
    try:
      html = helpers.get_content(url)
      if not html:
        return None

      soup = BeautifulSoup(html)

      headline = None
      potential_classes = ["heading-story", "articleOpinion-title"]
      for h1_class in potential_classes:
        try:
          headline = soup.find("h1", {"class": h1_class}).string
          break
        except AttributeError:
          continue
      if not headline:
        logger.log.error(
            'Exception trying to scrape Al Jazeera headline from %s' % (url))
        return None

      headline = helpers.decode(headline)

      try:
        paragraphs = soup.find("div", {"class": "article-body"})
        article = paragraphs.findAll("p")
      except AttributeError:
        paragraphs = soup.find("div", {"class": "text"})
        article = paragraphs.findAll("p")
      body = ' '.join([helpers.decode(p.text) for p in article])

      try:
        date = soup.find("time").string
      except AttributeError:
        date = soup.find("span", {"class": "date"}).string

      headline = helpers.decode(headline)
      body = helpers.decode(body)
      date = helpers.decode(date)
      return news_interface.Article(headline, body, url, news_orgs.ALJAZEERA,
                                    date)
    except Exception as e:
      logger.log.info("Hit exception getting article for %s: %s" % (url, e))

  def get_query_results(self, query):
    '''Implementation for keyword searches from Al Jazeera.

    Args:
      query: A URL-encoded string.

    Returns:
      A list of the top Articles returned by the query search.
    '''
    res = requests.get("https://www.googleapis.com/customsearch/v1element?key=AIzaSyCVAXiUzRYsML1Pv6RwSG1gunmMikTzQqY&rsz=filtered_cse&num=10&hl=en&prettyPrint=false&source=gcsc&gss=.com&sig=23952f7483f1bca4119a89c020d13def&cx=007864276874919660377:szp4pg3raxu&q=%s&lr=lang_en&filter=1&sort=&googlehost=www.google.com&callback=google.search.Search.apiary7638&nocache=1422548009762" % (query))

    json_res = res.text.encode('ascii', 'ignore')[48:-2]
    json_res = json.loads(json_res)['results']
    article_urls = [result['url'] for result in json_res]
    top_articles = []
    for url in article_urls[0:news_interface.NUM_ARTICLES]:
      if 'topics' not in url and 'blogs' not in url: # not an article page
        top_articles.append(self.get_article(url))
    return top_articles
