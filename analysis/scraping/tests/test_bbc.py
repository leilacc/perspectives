import logging
import unittest

from logger import log
import news_interface
import bbc

class TestBBC(unittest.TestCase):

  def setUp(self):
    self.BBC = bbc.BBC()

  def test_get_article(self):
    url = 'http://www.bbc.co.uk/news/world-europe-30808284'
    article = self.BBC.get_article(url)
    self.assertTrue(isinstance(article, news_interface.Article),
        'Expected the result to be an Article instance')
    self.assertEqual(article.headline,
                     'Charlie Hebdo attack: Print run for new issue expanded')
    self.assertEqual(article.date, '14 January 2015')

  def test_get_query_results(self):
    query = 'charlie+hebdo'
    res = self.BBC.get_query_results(query)
    self.assertEqual(len(res), news_interface.NUM_ARTICLES,
        'Expected %d articles' % news_interface.NUM_ARTICLES)
    self.assertTrue(isinstance(res[0], news_interface.Article),
        'Expected the result to be an Article instance')

if __name__ == '__main__':
  unittest.main()
