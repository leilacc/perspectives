import json

import api_keys
import helpers
import news_interface
import news_orgs


class NYTimes(news_interface.NewsOrg):
  '''Methods for interacting with the NYTimes website/API.'''

  def __init__(self):
    self.news_org = news_orgs.NY_TIMES
    self.search_url = ('http://api.nytimes.com/svc/search/v2/articlesearch.js' +
                       'on?q=%s&api-key=' +
                       api_keys.api_keys[news_orgs.NY_TIMES])

  def __repr__(self):
    return self.news_org

  def get_headline(self, soup):
    headline = helpers.decode(soup.h1.string)
    return headline

  def get_body(self, soup):
    try:
      article = soup.find('div', attrs={'class': 'articleBody'})
      paragraphs = article.find_all('p', attrs={'itemprop': 'articleBody'})
    except AttributeError:
      # this article's html uses different attributes... sigh...
      # Hopefully there are only 2 versions
      article = soup.find('div', attrs={'class': 'story-body'})
      paragraphs = article.find_all('p', attrs={'class': 'story-content'})

    p_text = [helpers.decode(p.get_text()) for p in paragraphs]
    body = ' '.join([p for p in p_text])
    return body

  def get_date(self, soup):
    try:
      date = soup.find('h6', attrs={'class': 'dateline'}).string
    except AttributeError:
      date = soup.find('time', attrs={'class': 'dateline'}).string
    return date

  def process_search_results(self, res):
    results = json.loads(res.text)['response']['docs']
    # web_urls have this weird '\/' instead of '/' for some reason
    article_urls = [res['web_url'].replace('\/', '/') for res in results]
    return article_urls
