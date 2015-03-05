import unittest

import news_interface
import russia_today

class TestRussiaToday(unittest.TestCase):

  def setUp(self):
    self.RussiaToday = russia_today.RussiaToday()

  def test_get_article(self):
    url = 'http://rt.com/news/226531-charlie-hebdo-isis-attacks/'
    article = self.RussiaToday.get_article(url)
    self.assertTrue(isinstance(article, news_interface.Article),
        'Expected the result to be an Article instance')
    self.assertEqual(article.headline,
                     "ISIS urges new attacks on infidel West following "
                     "Charlie Hebdo massacre")
    self.assertEqual(article.date, 'Published time: January 27, 2015 13:16')

  def test_get_query_results(self):
    query = 'charlie+hebdo'
    res = self.RussiaToday.get_query_results(query)
    self.assertEqual(len(res), news_interface.NUM_ARTICLES,
        'Expected %d articles' % news_interface.NUM_ARTICLES)
    self.assertTrue(isinstance(res[0], news_interface.Article),
        'Expected the result to be an Article instance')

if __name__ == '__main__':
  unittest.main()
