import unittest

import news_interface
import times_of_israel

class TestTimesOfIsrael(unittest.TestCase):

  def setUp(self):
    self.TimesOfIsrael = times_of_israel.TimesOfIsrael()

  def test_get_article_news(self):
    url = 'http://www.timesofisrael.com/nuclear-deal-with-west-very-close-zarif-says/'
    article = self.TimesOfIsrael.get_article(url)
    self.assertTrue(isinstance(article, news_interface.Article),
        'Expected the result to be an Article instance')
    self.assertEqual(article.headline,
                     "Nuclear deal with West 'very close', Zarif says")
    self.assertEqual(article.date, 'March 5, 2015, 12:29 am')

  def test_get_query_results(self):
    query = 'charlie+hebdo'
    res = self.TimesOfIsrael.get_query_results(query)
    self.assertEqual(len(res), news_interface.NUM_ARTICLES,
        'Expected %d articles' % news_interface.NUM_ARTICLES)
    self.assertTrue(isinstance(res[0], news_interface.Article),
        'Expected the result to be an Article instance')

if __name__ == '__main__':
  unittest.main()
