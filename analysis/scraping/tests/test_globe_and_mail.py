import logging
import unittest

from logger import log
import news_interface
import globe_and_mail

class TestGlobeAndMail(unittest.TestCase):

  def setUp(self):
    self.GlobeAndMail = globe_and_mail.GlobeAndMail()

  def test_get_article(self):
    url = 'http://www.theglobeandmail.com/news/world/grade-6-student-killed-by-us-drone-strike-in-yemen-rights-group-says/article22648002/'
    article = self.GlobeAndMail.get_article(url)
    self.assertTrue(isinstance(article, news_interface.Article),
        'Expected the result to be an Article instance')
    self.assertEqual(article.headline,
                     'Grade 6 student killed by U.S. drone strike in Yemen, '
                     'rights group says')
    self.assertEqual(article.date, 'Tuesday, Jan. 27 2015, 9:42 AM EST')

  def test_get_query_results(self):
    query = 'charlie+hebdo'
    res = self.GlobeAndMail.get_query_results(query)
    self.assertEqual(len(res), news_interface.NUM_ARTICLES,
        'Expected %d articles' % news_interface.NUM_ARTICLES)
    self.assertTrue(isinstance(res[0], news_interface.Article),
        'Expected the result to be an Article instance')

if __name__ == '__main__':
  unittest.main()
