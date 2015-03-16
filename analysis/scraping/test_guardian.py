import logging
import unittest

from logger import log
import news_interface
import guardian

class TestGuardian(unittest.TestCase):

  def setUp(self):
    self.Guardian = guardian.Guardian()

  def test_get_article(self):
    url = 'http://www.theguardian.com/sport/2015/jan/25/kevin-pietersen-england-surrey-de-register'
    article = self.Guardian.get_article(url)
    self.assertTrue(isinstance(article, news_interface.Article),
        'Expected the result to be an Article instance')
    self.assertEqual(article.headline,
                     "Kevin Pietersens England hopes hit again as Surrey rule "
                     "out return")
    self.assertEqual(article.date, 'Sunday 25 January 2015')

  def test_get_query_results(self):
    query = 'charlie+hebdo'
    res = self.Guardian.get_query_results(query)
    self.assertEqual(len(res), news_interface.NUM_ARTICLES,
        'Expected %d articles' % news_interface.NUM_ARTICLES)
    self.assertTrue(isinstance(res[0], news_interface.Article),
        'Expected the result to be an Article instance')

if __name__ == '__main__':
  unittest.main()
