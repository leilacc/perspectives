import logging
import unittest

from logger import log
import news_interface
import huff_post

class TestHuffPost(unittest.TestCase):

  def setUp(self):
    self.HuffPost = huff_post.HuffPost()

  def test_get_article(self):
    url = 'http://www.huffingtonpost.com/2015/01/18/charlie-hebdo-cartoons_n_6496414.html'
    article = self.HuffPost.get_article(url)
    self.assertTrue(isinstance(article, news_interface.Article),
        'Expected the result to be an Article instance')

  def test_get_query_results(self):
    query = 'charlie+hebdo'
    res = self.HuffPost.get_query_results(query)
    self.assertEqual(len(res), news_interface.NUM_ARTICLES,
        'Expected %d articles' % news_interface.NUM_ARTICLES)
    self.assertTrue(isinstance(res[0], news_interface.Article),
        'Expected the result to be an Article instance')

if __name__ == '__main__':
  unittest.main()
