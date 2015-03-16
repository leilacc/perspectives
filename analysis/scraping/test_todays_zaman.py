import unittest

import news_interface
import todays_zaman

class TestTodaysZaman(unittest.TestCase):

  def setUp(self):
    self.TodaysZaman = todays_zaman.TodaysZaman()

  def test_get_article_news(self):
    url = 'http://www.todayszaman.com/national_turkish-jetliner-skids-off-on-runway-in-kathmandu-passengers-safe_374261.html'
    article = self.TodaysZaman.get_article(url)
    self.assertTrue(isinstance(article, news_interface.Article),
        'Expected the result to be an Article instance')
    self.assertEqual(article.headline,
                     "Turkish jetliner skids off on runway in Kathmandu, "
                     "passengers safe")
    self.assertEqual(article.date, 'March 04, 2015, Wednesday/ 11:10:46/')

  def test_get_query_results(self):
    query = 'charlie+hebdo'
    res = self.TodaysZaman.get_query_results(query)
    self.assertEqual(len(res), news_interface.NUM_ARTICLES,
        'Expected %d articles' % news_interface.NUM_ARTICLES)
    self.assertTrue(isinstance(res[0], news_interface.Article),
        'Expected the result to be an Article instance')

if __name__ == '__main__':
  unittest.main()
