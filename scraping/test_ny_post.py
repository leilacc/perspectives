import logging
import unittest

from logger import log
import news_interface
import ny_post

class TestNYPost(unittest.TestCase):

  def setUp(self):
    self.NYPost = ny_post.NYPost()

  def test_get_article(self):
    url = 'http://nypost.com/2015/01/25/paris-terrorists-fit-profile-of-homegrown-threat-described-in-2007-nypd-report/'
    article = self.NYPost.get_article(url)
    self.assertTrue(isinstance(article, news_interface.Article),
        'Expected the result to be an Article instance')

  def test_get_query_results(self):
    query = 'charlie+hebdo'
    res = self.NYPost.get_query_results(query)
    self.assertEqual(len(res), news_interface.NUM_ARTICLES,
        'Expected %d articles' % news_interface.NUM_ARTICLES)
    self.assertTrue(isinstance(res[0], news_interface.Article),
        'Expected the result to be an Article instance')

if __name__ == '__main__':
  unittest.main()
