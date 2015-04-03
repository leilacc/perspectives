import logging
import unittest

from logger import log
import news_interface
import reuters

class TestReuters(unittest.TestCase):

  def setUp(self):
    self.REUTERS = reuters.Reuters()

  def test_get_article(self):
    url = 'http://www.reuters.com/article/2015/03/04/cnews-us-ukraine-crisis-mine-blast-idCAKBN0M00KR20150304'
    article = self.REUTERS.get_article(url)
    self.assertTrue(isinstance(article, news_interface.Article),
        'Expected the result to be an Article instance')
    self.assertEqual(article.headline,
                     "Thirty-three miners dead after pit blast in east Ukraine")
    self.assertEqual(article.date, 'Wed Mar 4, 2015 3:23pm EST')

  def test_get_query_results(self):
    query = 'charlie+hebdo'
    res = self.REUTERS.get_query_results(query)
    self.assertEqual(len(res), news_interface.NUM_ARTICLES,
        'Expected %d articles' % news_interface.NUM_ARTICLES)
    self.assertTrue(isinstance(res[0], news_interface.Article),
        'Expected the result to be an Article instance')

if __name__ == '__main__':
  unittest.main()
