import news_interface

class NewYorkPost(news_interface.NewsOrg):
  '''Methods for interacting with the New York Post website.

  Example usage:
  >>> import new_york_post
  >>> nyp = new_york_post.NewYorkPost()
  >>> nyp.get_article('')
  'got it'
  '''

  def get_article(self, url):
    '''Implementation for getting an article from the New York Post.'''
    return 'got it'

  def get_query_results(self, query):
    '''Implementation for getting an article from the New York Post.'''
    return 'got them'
