'''Get perspectives from different articles.'''

from scraping import logger
import re

import compare_articles
import extract_keywords
from scraping import aljazeera, bbc, cbc, cnn, globe_and_mail, guardian, \
                     huff_post, jpost, ny_post, ny_times

def get_perspectives(article):
  '''Get different perspectives on the topic covered by article.

  Args:
    article: an Article.

  Returns:
    A JSON-encoded string representing other articles with different
    perspectives than the original article.

    Format: a list of Article.to_dict()s, each with an additional 'sentences'
    attribute. 'sentences' contains a list of sentences with semantically
    different words that were extracted from the corresponding article's body.
  '''
  article_topic = extract_keywords.extract_keywords(article.headline)
  related_articles = query_all_news_orgs(article_topic)
  return compare_articles.compare.to_all_articles(article, related_articles)

def url_to_article(url):
  '''Returns the Article at url if the url is supported.

  Args:
    url: A string.

  Returns:
    The Article that is scraped from url, if the url corresponds to an article
    on a supported news org page. Otherwise, None.
  '''
  try:
    if re.search(r'.*aljazeera\.com/((opinions)|(articles)|(news))/.+', url):
      return aljazeera.AlJazeera().get_article(url)
    elif re.search(r'.*bbc\..+', url):
      return bbc.BBC().get_article(url)
    elif re.search(r'.*cbc\.ca/news/.+', url):
      return cbc.CBC().get_article(url)
    elif re.search(r'.*cnn\.com/.+', url):
      return cnn.CNN().get_article(url)
    elif re.search(r'.*theglobeandmail\.com/.+', url):
      return globe_and_mail.GlobeAndMail().get_article(url)
    elif re.search(r'.*theguardian\.com/.+', url):
      return guardian.Guardian().get_article(url)
    elif re.search(r'.*huffingtonpost\.c.+/.+', url):
      return huff_post.HuffPost().get_article(url)
    elif re.search(r'.*jpost\.com/.+', url):
      return jpost.JPost().get_article(url)
    elif re.search(r'.*nypost\.com/.+', url):
      return ny_post.NYPost().get_article(url)
    elif re.search(r'.*nytimes\.com/.+', url):
      return ny_times.NYTimes().get_article(url)
    else:
      logger.log.info("Didn't regexp match for %s" % url)
  except Exception as e:
    logger.log.info("Hit exception getting article for %s: %s" % (url, e))
    return None

def query_all_news_orgs(query):
  '''Get the top articles for the given query from all supported news orgs.

  Args:
    query: A string of keywords.

  Returns:
    A list of Articles.
  '''
  return #TODO: complete
