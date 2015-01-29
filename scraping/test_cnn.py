import logging
import unittest

from logger import log
import news_interface
import cnn

class TestCNN(unittest.TestCase):

  def setUp(self):
    self.CNN = cnn.CNN()

  def test_get_article(self):
    url = 'http://www.cnn.com/2015/01/27/us/mormon-church-lgbt-laws/index.html' #'http://www.bbc.co.uk/news/world-europe-30808284'
    article = self.CNN.get_article(url)
    self.assertTrue(isinstance(article, news_interface.Article),
        'Expected the result to be an Article instance')

#  def test_get_query_results(self):
 #   query = 'charlie+hebdo'
  #  res = self.BBC.get_query_results(query)
  #  self.assertEqual(len(res), news_interface.NUM_ARTICLES,
   #     'Expected %d articles' % news_interface.NUM_ARTICLES)
   # self.assertTrue(isinstance(res[0], news_interface.Article),
    #    'Expected the result to be an Article instance')

if __name__ == '__main__':
  unittest.main()






