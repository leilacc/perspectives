import unittest

import perspectives
from scraping import news_interface

class TestPerspectives(unittest.TestCase):

  def test_url_to_article_aljazeera(self):
    article = perspectives.url_to_article(
        'http://www.aljazeera.com/news/middleeast/2015/01/japanese-hostage-beheaded-isil-150131201857344.html')
    self.assertTrue(isinstance(article, news_interface.Article))
    self.assertEqual(article.headline,
                     "Second Japanese hostage 'beheaded' by ISIL in video")

if __name__ == '__main__':
  unittest.main()
