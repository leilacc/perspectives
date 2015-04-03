import xmltodict

import api_keys
import helpers
import logger
import news_interface
import news_orgs


class USAToday(news_interface.NewsOrg):
  '''Methods for interacting with the USA Today website/API.'''

  def __init__(self):
    self.news_org = news_orgs.USA_TODAY
    self.search_url = ("http://api.usatoday.com/open/articles?keyword=%s&" +
                       "api_key=" + api_keys.api_keys[news_orgs.USA_TODAY])

  def __repr__(self):
    return self.news_org

  def get_headline(self, soup):
    headline = soup.article.h1.string
    return headline

  def get_body(self, soup):
    article = soup.article
    paragraphs = article.find_all('p', attrs={'class': None})
    body = ' '.join([helpers.decode(p.get_text()) for p in paragraphs])
    return body

  def get_date(self, soup):
    time_span = soup.find('span', attrs={'class': 'asset-metabar-time'})
    date = time_span.contents[0]
    return date

  def process_search_results(self, res):
    xml_dict = xmltodict.parse(res.text)

    try:
      all_articles = xml_dict['rss']['channel']['item']
    except KeyError:
      logger.log.error(res.text)

    return [article['link'] for article in all_articles]
