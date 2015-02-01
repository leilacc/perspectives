import logging
import unittest

from logger import log
import news_interface
import cbc

class TestCBC(unittest.TestCase):

  def setUp(self):
    self.CBC = cbc.CBC()

  def test_get_article(self):
    url = 'http://www.cbc.ca/news/world/greek-election-left-wing-syriza-party-wins-but-number-of-seats-in-question-1.2930923'
    article = self.CBC.get_article(url)
    self.assertTrue(isinstance(article, news_interface.Article),
        'Expected the result to be an Article instance')

  def test_get_query_results(self):
    query = 'charlie+hebdo'
    res = self.CBC.get_query_results(query)
    self.assertEqual(len(res), news_interface.NUM_ARTICLES,
        'Expected %d articles' % news_interface.NUM_ARTICLES)
    self.assertTrue(isinstance(res[0], news_interface.Article),
        'Expected the result to be an Article instance')

if __name__ == '__main__':
  unittest.main()
