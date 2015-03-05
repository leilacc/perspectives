import logging
import unittest

from logger import log
import news_interface
import aljazeera

class TestAlJazeera(unittest.TestCase):

  def setUp(self):
    self.AlJazeera = aljazeera.AlJazeera()

  def test_get_article(self):
    url = 'http://www.aljazeera.com/indepth/opinion/2015/01/charlie-hebdo-us-them-201511152114498897.html'
    article = self.AlJazeera.get_article(url)
    self.assertTrue(isinstance(article, news_interface.Article),
        'Expected the result to be an Article instance')
    self.assertEqual(article.headline, "Charlie Hebdo: 'Us or them'")
    self.assertEqual(article.date, "11 Jan 2015 13:35 GMT")

  def test_get_query_results(self):
    query = 'charlie+hebdo'
    res = self.AlJazeera.get_query_results(query)
    self.assertEqual(len(res), news_interface.NUM_ARTICLES,
        'Expected %d articles' % news_interface.NUM_ARTICLES)
    self.assertTrue(isinstance(res[0], news_interface.Article),
        'Expected the result to be an Article instance')

if __name__ == '__main__':
  unittest.main()
