import unittest

import news_interface
import usa_today

class TestUSAToday(unittest.TestCase):

  def setUp(self):
    self.USAToday = usa_today.USAToday()

  def test_get_article_news(self):
    url = 'http://www.usatoday.com/story/news/nation-now/2015/01/20/democrat-charlie-hebdo-tribute-obama-speech/22070673/'
    article = self.USAToday.get_article(url)
    self.assertTrue(isinstance(article, news_interface.Article),
        'Expected the result to be an Article instance')

  def test_get_article_travel(self):
    url = 'http://www.usatoday.com/story/travel/columnist/greatamericanbites/2015/01/22/dierks-bently-whiskey-row-scottsdale/22112457/'
    article = self.USAToday.get_article(url)
    self.assertTrue(isinstance(article, news_interface.Article),
        'Expected the result to be an Article instance')

  def test_get_query_results(self):
    query = 'charlie+hebdo'
    res = self.USAToday.get_query_results(query)
    self.assertEqual(len(res), news_interface.NUM_ARTICLES,
        'Expected %d articles' % news_interface.NUM_ARTICLES)
    self.assertTrue(isinstance(res[0], news_interface.Article),
        'Expected the result to be an Article instance')

if __name__ == '__main__':
  unittest.main()
