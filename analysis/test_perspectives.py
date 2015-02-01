import unittest

import perspectives
from scraping import news_interface

class TestPerspectives(unittest.TestCase):

  def _test_url_to_article(self, url, headline):
    article = perspectives.url_to_article(url)
    self.assertTrue(isinstance(article, news_interface.Article))
    self.assertEqual(article.headline, headline)

  def test_url_to_article_aljazeera(self):
    url = 'http://www.aljazeera.com/news/middleeast/2015/01/japanese-hostage-beheaded-isil-150131201857344.html'
    headline = "Japan says ISIL beheading video likely authentic"
    self._test_url_to_article(url, headline)

  def test_url_to_article_bbc(self):
    url = 'http://www.bbc.co.uk/news/uk-31079515'
    headline = "Nicky Morgan announces 'war on illiteracy and innumeracy'"
    self._test_url_to_article(url, headline)

  def test_url_to_article_cbc(self):
    url = 'http://www.cbc.ca/news/canada/ottawa/shots-fired-in-carlington-area-should-lead-to-charges-police-say-1.2939073'
    headline = "Shots fired in Carlington area should lead to charges, police say"
    self._test_url_to_article(url, headline)

  def test_url_to_article_cnn(self):
    url = 'http://www.cnn.com/2015/01/31/entertainment/taiwan-scorcese-movie-set-accident/index.html'
    headline = "One killed, 2 injured on set of Martin Scorsese's movie 'Silence' "
    self._test_url_to_article(url, headline)

  def test_url_to_article_globe_and_mail(self):
    url = 'http://www.theglobeandmail.com/globe-debate/syria-the-worlds-most-dangerous-place-for-journalists/article22732947/'
    headline = "Syria: The worlds most dangerous place for journalists"
    self._test_url_to_article(url, headline)

  def test_url_to_article_guardian(self):
    url = 'http://www.theguardian.com/us-news/2015/feb/01/carl-djerassi-chemist-considered-father-of-birth-control-pill-dies-at-age-91-0'
    headline = "Carl Djerassi, chemist who developed the birth control pill, dies at age 91"
    self._test_url_to_article(url, headline)

  def test_url_to_article_huff_post(self):
    url = 'http://www.huffingtonpost.ca/jeffrey-schwartz/disability-and-debt_b_6582328.html'
    headline = "Disability and Debt: When One Happens to Canadians, the Other Follows"
    self._test_url_to_article(url, headline)

if __name__ == '__main__':
  unittest.main()
