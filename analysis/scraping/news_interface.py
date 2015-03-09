import sys

NUM_ARTICLES = 2

def _functionId(obj, nFramesUp):
    '''Create a string naming the function n frames up on the stack.'''
    fr = sys._getframe(nFramesUp+1)
    co = fr.f_code
    return "%s.%s" % (obj.__class__, co.co_name)

def abstractMethod(obj=None):
    '''Use this instead of 'pass' for the body of abstract methods.'''
    raise Exception("Unimplemented abstract method: %s" % _functionId(obj, 1))

class NewsOrg:
  '''Represents a news organization.'''

  def get_article(self, url):
    '''Return an Article representing the article at url.'''
    abstractMethod(self)

  def get_query_results(self, query):
    '''Return a list of NUM_ARTICLES Articles returned by query.

    query: A URL-encoded string.
    '''
    abstractMethod(self)

class Article:
  '''Represents an article.'''

  def __init__(self, headline, body, link, news_org, date):
    '''Initialize the article's properties.

    headline: str
    body: str
    link: str
    news_org: str. See the macros in api_keys
    date: str, unaltered from scraping
    '''
    self.headline = headline
    self.body = body
    self.link = link
    self.news_org = news_org
    self.date = date

  def __repr__(self):
    '''Representation of the article.'''
    return ('----------------------------------------------------------------\n'
            'ARTICLE\n'
            'Org: %s\n'
            'Headline: %s...\n'
            'Date: %s\n'
            'Body: %s...\n'
            'Link: %s\n'
            % (self.news_org, self.headline[0:66], self.date,
               self.body[0:70], self.link))

  def to_dict(self):
    '''Return the Article represented in dictionary form.

    article: an Article

    Returns: A dictionary representation of the article.
    '''
    article_dict = {}
    article_dict["headline"] = self.headline
    article_dict["body"] = self.body
    article_dict["link"] = self.link
    article_dict["news_org"] = self.news_org
    article_dict["date"] = self.date
    return article_dict

