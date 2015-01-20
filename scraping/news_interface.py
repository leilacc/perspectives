import sys

def _functionId(obj, nFramesUp):
    """ Create a string naming the function n frames up on the stack. """
    fr = sys._getframe(nFramesUp+1)
    co = fr.f_code
    return "%s.%s" % (obj.__class__, co.co_name)

def abstractMethod(obj=None):
    """ Use this instead of 'pass' for the body of abstract methods. """
    raise Exception("Unimplemented abstract method: %s" % _functionId(obj, 1))

class NewsOrg:
  '''Represents a news organization.'''

  def get_article(self, url):
    '''Return the contents of the article at url.'''
    abstractMethod(self)

  def get_query_results(self, query):
    '''Return the results of the query in the news org's search system.'''
    abstractMethod(self)
