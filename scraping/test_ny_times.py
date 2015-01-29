import unittest

import news_interface
import ny_times

class TestNYTimes(unittest.TestCase):

  def setUp(self):
    self.NYTimes = ny_times.NYTimes()

  def test_get_article(self):
    url = 'http://query.nytimes.com/gst/fullpage.html?res=9D07E0D9103CF934A35752C1A9679D8B63'
    article = self.NYTimes.get_article(url)
    self.assertTrue(isinstance(article, news_interface.Article),
        'Expected the result to be an Article instance')

  def test_get_query_results(self):
    query = 'charlie+hebdo'
    res = self.NYTimes.get_query_results(query)
    self.assertEqual(len(res), news_interface.NUM_ARTICLES,
        'Expected %d articles' % news_interface.NUM_ARTICLES)
    self.assertTrue(isinstance(res[0], news_interface.Article),
        'Expected the result to be an Article instance')

if __name__ == '__main__':
  unittest.main()
