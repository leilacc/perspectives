import logging
import unittest

from logger import log
import news_interface
import bbc

class TestREUTERS(unittest.TestCase):

  def setUp(self):
    self.REUTERS = bbc.REUTERS()

  def test_get_article(self):
    url = 'http://www.bbc.co.uk/news/world-europe-30808284'
    article = self.BBC.get_article(url)
    self.assertTrue(isinstance(article, news_interface.Article),
        'Expected the result to be an Article instance')

  def test_get_query_results(self):
    query = 'charlie+hebdo'
    res = self.BBC.get_query_results(query)
    self.assertEqual(len(res), news_interface.NUM_ARTICLES,
        'Expected %d articles' % news_interface.NUM_ARTICLES)
    self.assertTrue(isinstance(res[0], news_interface.Article),
        'Expected the result to be an Article instance')

if __name__ == '__main__':
  unittest.main()
