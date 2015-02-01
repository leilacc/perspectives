import unittest

import perspectives
from scraping import news_interface

class TestPerspectives(unittest.TestCase):

  def test_url_to_article_aljazeera(self):
    article = perspectives.url_to_article(
        'http://www.aljazeera.com/news/middleeast/2015/01/japanese-hostage-beheaded-isil-150131201857344.html')
    self.assertTrue(isinstance(article, news_interface.Article))
    self.assertEqual(article.headline,
                     "Japan says ISIL beheading video likely authentic")

  def test_url_to_article_bbc(self):
    article = perspectives.url_to_article(
        'http://www.bbc.co.uk/news/uk-31079515')
    self.assertTrue(isinstance(article, news_interface.Article))
    self.assertEqual(article.headline,
                     "Nicky Morgan announces 'war on illiteracy and innumeracy'")

if __name__ == '__main__':
  unittest.main()
