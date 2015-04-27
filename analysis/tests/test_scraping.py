import unittest

import scraping.news_interface as news_interface
import scraping.aljazeera as aljazeera
import scraping.bbc as bbc
import scraping.cbc as cbc
import scraping.cnn as cnn
import scraping.globe_and_mail as globe_and_mail
import scraping.guardian as guardian
import scraping.huff_post as huff_post
import scraping.jpost as jpost
import scraping.ny_post as ny_post
import scraping.ny_times as ny_times
import scraping.reuters as reuters
import scraping.russia_today as russia_today
import scraping.times_of_israel as times_of_israel
import scraping.todays_zaman as todays_zaman
import scraping.usa_today as usa_today

class TestScraping(unittest.TestCase):

  @classmethod
  def setUpClass(cls):
    cls.AlJazeera = aljazeera.AlJazeera()
    cls.BBC = bbc.BBC()
    cls.CBC = cbc.CBC()
    cls.CNN = cnn.CNN()
    cls.GLOBE_AND_MAIL = globe_and_mail.GlobeAndMail()
    cls.GUARDIAN = guardian.Guardian()
    cls.HUFF_POST = huff_post.HuffPost()
    cls.JPOST = jpost.JPost()
    cls.NY_POST = ny_post.NYPost()
    cls.NY_TIMES = ny_times.NYTimes()
    cls.REUTERS = reuters.Reuters()
    cls.RUSSIA_TODAY = russia_today.RussiaToday()
    cls.TIMES_OF_ISRAEL = times_of_israel.TimesOfIsrael()
    cls.TODAYS_ZAMAN = todays_zaman.TodaysZaman()
    cls.USA_TODAY = usa_today.USAToday()

  def get_article(self, news_org, url, headline, date):
    article = news_org.get_article(url)
    self.assertTrue(isinstance(article, news_interface.Article),
        'Expected the result to be an Article instance')
    self.assertEqual(article.headline, headline)
    self.assertEqual(article.date, date)

  def get_query_results(self, news_org, query):
    res = news_org.get_query_results(query)
    self.assertEqual(len(res), news_interface.NUM_ARTICLES,
        'Expected %d articles' % news_interface.NUM_ARTICLES)
    self.assertTrue(isinstance(res[0], news_interface.Article),
        'Expected the result to be an Article instance')

  def test_aljazeera_get_article(self):
    news_org = self.AlJazeera
    url = 'http://www.aljazeera.com/indepth/opinion/2015/01/charlie-hebdo-us-them-201511152114498897.html'
    headline = "Charlie Hebdo: 'Us or them'"
    date = "11 Jan 2015 13:35 GMT"
    self.get_article(news_org, url, headline, date)

  def test_aljazeera_get_query_results(self):
    query = 'charlie+hebdo'
    news_org = self.AlJazeera
    self.get_query_results(news_org, query)

  def test_bbc_get_article(self):
    news_org = self.BBC
    url = 'http://www.bbc.co.uk/news/world-europe-30808284'
    headline = 'Charlie Hebdo attack: Print run for new issue expanded'
    date = '14 January 2015'
    self.get_article(news_org, url, headline, date)

  def test_bbc_get_query_results(self):
    query = 'charlie+hebdo'
    news_org = self.BBC
    self.get_query_results(news_org, query)

  def test_cbc_get_article(self):
    news_org = self.CBC
    url = 'http://www.cbc.ca/news/world/greek-election-left-wing-syriza-party-wins-but-number-of-seats-in-question-1.2930923'
    headline = ('Greek election: Left-wing Syriza party wins but number '
                'of seats in question')
    date = 'Posted: Jan 25, 2015 12:54 AM ET'
    self.get_article(news_org, url, headline, date)

  def test_cbc_get_query_results(self):
    query = 'charlie+hebdo'
    news_org = self.CBC
    self.get_query_results(news_org, query)

  def test_cnn_get_article(self):
    news_org = self.CNN
    url = 'http://www.cnn.com/2015/01/31/middleeast/isis-japan-jordan-hostages/index.html'
    headline = 'Video: ISIS purportedly beheads Japanese hostage'
    date = 'Updated 4:58 PM ET, Tue February 3, 2015'
    self.get_article(news_org, url, headline, date)

  def test_cnn_get_query_results(self):
    query = 'charlie+hebdo'
    news_org = self.CNN
    self.get_query_results(news_org, query)

  def test_globe_and_mail_get_article(self):
    news_org = self.GLOBE_AND_MAIL
    url = 'http://www.theglobeandmail.com/news/world/grade-6-student-killed-by-us-drone-strike-in-yemen-rights-group-says/article22648002/'
    headline = ('Grade 6 student killed by U.S. drone strike in Yemen, '
                'rights group says')
    date = 'Tuesday, Jan. 27 2015, 9:42 AM EST'
    self.get_article(news_org, url, headline, date)

  def test_globe_and_mail_get_query_results(self):
    query = 'charlie+hebdo'
    news_org = self.GLOBE_AND_MAIL
    self.get_query_results(news_org, query)

  def test_guardian_get_article(self):
    news_org = self.GUARDIAN
    url = 'http://www.theguardian.com/sport/2015/jan/25/kevin-pietersen-england-surrey-de-register'
    headline = ("Kevin Pietersen's England hopes hit again as Surrey rule "
                "out return")
    date = 'Sunday 25 January 2015'
    self.get_article(news_org, url, headline, date)

  def test_guardian_get_query_results(self):
    query = 'charlie+hebdo'
    news_org = self.GUARDIAN
    self.get_query_results(news_org, query)

  def test_huff_post_get_article(self):
    news_org = self.HUFF_POST
    url = 'http://www.huffingtonpost.com/2015/01/18/charlie-hebdo-cartoons_n_6496414.html'
    headline = ("Charlie Hebdo Editor Slams News Organizations For Not "
                "Publishing Cartoons")
    date = '01/18/2015 12:05 pm EST'
    self.get_article(news_org, url, headline, date)

  def test_huff_post_get_query_results(self):
    query = 'charlie+hebdo'
    news_org = self.HUFF_POST
    self.get_query_results(news_org, query)

  def test_jpost_get_article(self):
    news_org = self.JPOST
    url = 'http://www.jpost.com/Israel-News/Politics-And-Diplomacy/US-challenges-Israel-to-sharpen-alternative-path-on-Iranian-nuclear-negotiations-392974'
    headline = ("US challenges Israel to sharpen alternative path on "
                "Iranian nuclear negotiations")
    date = '03/05/2015 00:14'
    self.get_article(news_org, url, headline, date)

  def test_jpost_get_query_results(self):
    query = 'charlie+hebdo'
    news_org = self.JPOST
    self.get_query_results(news_org, query)

  def test_ny_post_get_article(self):
    news_org = self.NY_POST
    url = 'http://nypost.com/2015/01/25/paris-terrorists-fit-profile-of-homegrown-threat-described-in-2007-nypd-report/'
    headline = ("Paris terrorists fit profile of homegrown threat "
                "described in 2007 NYPD report")
    date = 'January 25, 2015 | 7:48am'
    self.get_article(news_org, url, headline, date)

  def test_ny_post_get_query_results(self):
    query = 'charlie+hebdo'
    news_org = self.NY_POST
    self.get_query_results(news_org, query)

  def test_ny_times_get_article(self):
    news_org = self.NY_TIMES
    url = 'http://query.nytimes.com/gst/fullpage.html?res=9D07E0D9103CF934A35752C1A9679D8B63'
    headline = ("MEDIA DECODER; A Provocative Newspaper Is Attacked in "
                "France, And Support Is Swift")
    date = 'Published: November 7, 2011'
    self.get_article(news_org, url, headline, date)

  def test_ny_times_get_query_results(self):
    query = 'charlie+hebdo'
    news_org = self.NY_TIMES
    self.get_query_results(news_org, query)

  def test_reuters_get_article(self):
    news_org = self.REUTERS
    url = 'http://www.reuters.com/article/2015/03/04/cnews-us-ukraine-crisis-mine-blast-idCAKBN0M00KR20150304'
    headline = "Thirty-three miners dead after pit blast in east Ukraine"
    date = 'Wed Mar 4, 2015 3:23pm EST'
    self.get_article(news_org, url, headline, date)

  def test_reuters_get_query_results(self):
    query = 'charlie+hebdo'
    news_org = self.REUTERS
    self.get_query_results(news_org, query)

  def test_russia_today_get_article(self):
    news_org = self.RUSSIA_TODAY
    url = 'http://rt.com/news/226531-charlie-hebdo-isis-attacks/'
    headline = ("ISIS urges new attacks on infidel West following "
                "Charlie Hebdo massacre")
    date = 'Published time: January 27, 2015 13:16'
    self.get_article(news_org, url, headline, date)

  def test_russia_today_get_query_results(self):
    query = 'charlie+hebdo'
    news_org = self.RUSSIA_TODAY
    self.get_query_results(news_org, query)

  def test_times_of_israel_get_article(self):
    news_org = self.TIMES_OF_ISRAEL
    url = 'http://www.timesofisrael.com/nuclear-deal-with-west-very-close-zarif-says/'
    headline = "Nuclear deal with West 'very close,' Zarif says"
    date = 'March 5, 2015, 12:29 am'
    self.get_article(news_org, url, headline, date)

  def test_times_of_israel_get_query_results(self):
    query = 'charlie+hebdo'
    news_org = self.TIMES_OF_ISRAEL
    self.get_query_results(news_org, query)

  def test_todays_zaman_get_article(self):
    news_org = self.TODAYS_ZAMAN
    url = 'http://www.todayszaman.com/national_turkish-jetliner-skids-off-on-runway-in-kathmandu-passengers-safe_374261.html'
    headline = ("Turkish jetliner skids off on runway in Kathmandu, "
                "passengers safe")
    date = 'March 04, 2015, Wednesday/ 11:10:46/'
    self.get_article(news_org, url, headline, date)

  def test_todays_zaman_get_query_results(self):
    query = 'charlie+hebdo'
    news_org = self.TODAYS_ZAMAN
    self.get_query_results(news_org, query)

  def test_usa_today_get_article(self):
    news_org = self.USA_TODAY
    url = 'http://www.usatoday.com/story/news/nation-now/2015/01/20/democrat-charlie-hebdo-tribute-obama-speech/22070673/'
    headline = "Democrat organizes 'Charlie Hebdo' tribute at Obama speech"
    date = '6:17 p.m. EST January 20, 2015'
    self.get_article(news_org, url, headline, date)

  def test_usa_today_get_query_results(self):
    query = 'charlie+hebdo'
    news_org = self.USA_TODAY
    self.get_query_results(news_org, query)

if __name__ == '__main__':
  unittest.main()
