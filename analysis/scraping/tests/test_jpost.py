import logging
import unittest

from logger import log
import news_interface
import jpost

class TestJPost(unittest.TestCase):

  def setUp(self):
    self.JPost = jpost.JPost()

  def test_get_article(self):
    url = 'http://www.jpost.com/Israel-News/Politics-And-Diplomacy/US-challenges-Israel-to-sharpen-alternative-path-on-Iranian-nuclear-negotiations-392974'
    article = self.JPost.get_article(url)
    self.assertTrue(isinstance(article, news_interface.Article),
        'Expected the result to be an Article instance')
    self.assertEqual(article.headline,
                     "US challenges Israel to sharpen alternative path on "
                     "Iranian nuclear negotiations")
    self.assertEqual(article.date, '03/05/2015 00:14')

  def test_get_query_results(self):
    query = 'charlie+hebdo'
    res = self.JPost.get_query_results(query)
    self.assertEqual(len(res), news_interface.NUM_ARTICLES,
        'Expected %d articles' % news_interface.NUM_ARTICLES)
    self.assertTrue(isinstance(res[0], news_interface.Article),
        'Expected the result to be an Article instance')

if __name__ == '__main__':
  unittest.main()
