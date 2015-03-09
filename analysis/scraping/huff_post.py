from bs4 import BeautifulSoup
import json
import logging
import requests

from . import api_keys
from . import helpers
from . import logger
from . import news_interface
from . import news_orgs

logging.basicConfig(filename='huff_post.log', level=logging.WARNING)

class HuffPost(news_interface.NewsOrg):
  '''Methods for interacting with the Huffington Post website/API.'''

  def get_article(self, url):
    '''Implementation for getting an article from Huffington Post.

    Args:
      url: A URL in the www.huffingtonpost.* domain.

    Returns:
      The Article representing the article at that url.
    '''
    try:
      html = helpers.get_content(url)
      if not html:
        return None

      soup = BeautifulSoup(html)
      headline = soup.h1.string
      article = soup.find('article', attrs={'class': 'entry'})
      paragraphs = article.find_all('p', attrs={'class': None})
      body = ' '.join([p.get_text() for p in paragraphs])
      date = soup.find('span', attrs={'class': 'posted'}).find('time').string

      headline = helpers.decode(headline)
      body = helpers.decode(body)
      date = helpers.decode(date)
      return news_interface.Article(headline, body, url, news_orgs.HUFF_POST,
                                    date)
    except Exception as e:
      logger.log.info("Hit exception getting article for %s: %s" % (url, e))

  def get_query_results(self, query):
    '''Implementation for keyword searches from Huffington Post.

    Args:
      query: A URL-encoded string.

    Returns:
      A list of the top Articles returned by the query search.
    '''
    res = requests.get(
        'https://www.googleapis.com/customsearch/v1element?key=%s&rsz=10&num=10&hl=en&prettyPrint=false&source=gcsc&gss=.com&sig=23952f7483f1bca4119a89c020d13def&cx=004830092955692134028:an6per91wyc&q=%s&as_sitesearch=huffingtonpost.com&googlehost=www.google.com&callback=google.search.Search.apiary17234&nocache=1422138917068'
        % (api_keys.api_keys[news_orgs.HUFF_POST], query))
    results = json.loads(res.text[49:-2])['results']
    article_urls = [res['url'] for res in results]

    top_articles = []
    for url in article_urls:
      if url.endswith('.html'):
        # Huff Post sometimes returns aggregator pages that don't
        # contain an article and don't end in .html
        top_articles.append(self.get_article(url))
    return top_articles[0:news_interface.NUM_ARTICLES]
