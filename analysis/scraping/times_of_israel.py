from bs4 import BeautifulSoup
import logging
import requests
import urllib2

import helpers
from logger import log
import news_interface
import news_orgs

logging.basicConfig(filename='times_of_israel.log', level=logging.WARNING)

class TimesOfIsrael(news_interface.NewsOrg):
  '''Methods for interacting with the Times of Israel website.'''

  def get_article(self, url):
    '''Implementation for getting an article from Times of Israel.

    Args:
      url: A URL in the www.timesofisrael.com/* domain.

    Returns:
      The Article representing the article at that url.
    '''
    try:
      html = helpers.get_content(url)
      if not html:
        return None

      soup = BeautifulSoup(html)
      h1 = soup.find('h1', attrs={'class': 'headline'})
      headline = helpers.decode(h1.text)
      paragraphs = soup.findAll("p", {"itemprop": "articleBody"})
      body = ' '.join([helpers.decode(p.text) for p in paragraphs])
      date = helpers.decode(
          soup.find('span', attrs={'class': 'date'}).getText())

      return news_interface.Article(headline, body, url,
                                    news_orgs.TIMES_OF_ISRAEL, date)
    except Exception as e:
      log.info("Hit exception getting article for %s: %s" % (url, e))

  def get_query_results(self, query):
    '''Implementation for keyword searches from Times of Israel.

    Args:
      query: A URL-encoded string.

    Returns:
      A list of the top Articles returned by the query search.
    '''
    res = requests.get("https://www.googleapis.com/customsearch/v1element?key=AIzaSyCVAXiUzRYsML1Pv6RwSG1gunmMikTzQqY&rsz=filtered_cse&num=10&hl=en&prettyPrint=false&source=gcsc&gss=.com&sig=23952f7483f1bca4119a89c020d13def&cx=015742192883069867459:k3m1yn-i4ua&q=%s&googlehost=www.google.com&callback=google.search.Search.apiary782&nocache=1422549552720" % (query))

    output = res.text.encode('ascii', 'ignore').split("\"ogUrl\":")
    article_urls = []
    for line in output:
      try:
        a = line.split(",")[0].replace('"',"")
        if "http" in a:
          article_urls.append(a)
      except:
        pass

    top_articles = []
    for url in article_urls[0:news_interface.NUM_ARTICLES]:
      top_articles.append(self.get_article(url))
    return top_articles
