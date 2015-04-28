import json
import unittest

import perspectives
from scraping import news_interface

class TestPerspectives(unittest.TestCase):

  def test_get_perspectives(self):
    url = 'http://jpost.com/Israel-News/ICC-rejects-pro-Turkey-war-crimes-allegations-against-IDF-in-Gaza-flotilla-raid-380955'
    res = perspectives.get_perspectives(url)
    compared_articles = json.loads(res)
    length = len(compared_articles)
    self.assertTrue(length > 5, 'Length is %s' % length)
    self.assertTrue(compared_articles[0]['sentences'],
                    'Result not of expected format')

  def test_get_perspectives_non_article(self):
    url = 'http://facebook.com/'
    res = json.loads(perspectives.get_perspectives(url))
    self.assertEqual(res, {'Error': 'Not a recognized article'})

    '''
  def test_query_all_news_orgs(self):
    query = 'charlie+hebdo'
    articles = perspectives.query_all_news_orgs(query)
    self.assertTrue(len(articles) > 10)
    for article in articles:
      if article:
        self.assertTrue(isinstance(article, news_interface.Article))

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
    headline = "One killed, 2 injured on set of Martin Scorsese's movie 'Silence'"
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

  def test_url_to_article_jpost(self):
    url = 'http://www.jpost.com/Opinion/Irans-nuclear-program-is-a-threat-389579'
    headline = "Irans nuclear program is a threat"
    self._test_url_to_article(url, headline)

  def test_url_to_article_ny_post(self):
    url = 'http://nypost.com/2015/01/31/why-picking-a-super-bowl-side-is-such-a-nightmare/'
    headline = "Why picking a Super Bowl side is such a nightmare"
    self._test_url_to_article(url, headline)

  def test_url_to_article_ny_times(self):
    url = 'http://www.nytimes.com/2015/02/01/style/sundance-courts-a-new-celebrity-crowd.html?action=click&pgtype=Homepage&module=c-column-middle-span-region&region=c-column-middle-span-region&WT.nav=c-column-middle-span-region&_r=0'
    headline = "Sundance Courts a New Celebrity Crowd"
    self._test_url_to_article(url, headline)

  def test_url_to_article_reuters(self):
    url = 'http://www.reuters.com/article/2015/01/31/us-indonesia-airplane-idUSKBN0L404E20150131'
    headline = "AirAsia captain left seat before jet lost control: sources"
    self._test_url_to_article(url, headline)

  def test_url_to_article_rt(self):
    url = 'http://rt.com/uk/228227-british-army-psychological-warfare/'
    headline = "New British army elite unit to hone social media and psychological warfare"
    self._test_url_to_article(url, headline)

  def test_url_to_article_times_of_israel(self):
    url = 'http://www.timesofisrael.com/in-super-bowl-matchup-pats-have-israel-connections-cornered/'
    headline = "In Super Bowl matchup, Pats have Israel connections covered"
    self._test_url_to_article(url, headline)

  def test_url_to_article_todays_zaman(self):
    url = 'http://www.todayszaman.com/interviews_speaking-of-islamo-christian-civilization-amidst-turmoil-of-clash-of-civilizations_371243.html'
    headline = "Speaking of Islamo-Christian civilization amidst turmoil of clash of civilizations"
    self._test_url_to_article(url, headline)

  def test_url_to_article_usa_today(self):
    url = 'http://www.usatoday.com/story/todayinthesky/2015/01/31/airlines-already-canceling-flights-as-new-storm-looms/22682285/'
    headline = "Airlines already canceling flights as new storm looms"
    self._test_url_to_article(url, headline)

if __name__ == '__main__':
  unittest.main()
