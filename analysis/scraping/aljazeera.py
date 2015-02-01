from bs4 import BeautifulSoup
import logging
import re
import requests
import urllib2

from logger import log
import news_interface
import news_orgs

logging.basicConfig(filename='aljazeera.log', level=logging.WARNING)

class AlJazeera(news_interface.NewsOrg):
  '''Methods for interacting with the Al Jazeera website.'''

  def get_article(self, url):
    '''Implementation for getting an article from Al Jazeera.

    Args:
      url: A URL in the www.aljazeera.* domain.

    Returns:
      The Article representing the article at that url.
    '''
    response = urllib2.urlopen(url)
    html = response.read()
    soup = BeautifulSoup(html)
    a = soup.find("title")
    headline = a.text

    paragraphs = soup.find("div", {"class": "text section"})
    article = paragraphs.findAll("p")
    body = ' '.join([p.text.encode('ascii', 'ignore') for p in article])
    log.info(headline)
    log.info(body)
    return news_interface.Article(headline, body, url, news_orgs.ALJAZEERA)

  def get_query_results(self, query):
   '''Implementation for keyword searches from Al Jazeera.

    Args:
      query: A URL-encoded string.

    Returns:
      A list of the top Articles returned by the query search.
    '''
   res = requests.get("https://www.googleapis.com/customsearch/v1element?key=AIzaSyCVAXiUzRYsML1Pv6RwSG1gunmMikTzQqY&rsz=filtered_cse&num=10&hl=en&prettyPrint=false&source=gcsc&gss=.com&sig=23952f7483f1bca4119a89c020d13def&cx=007864276874919660377:szp4pg3raxu&q=%s&lr=lang_en&filter=1&sort=&googlehost=www.google.com&callback=google.search.Search.apiary7638&nocache=1422548009762" % (query))

   output = res.text.encode('ascii', 'ignore').split("\"ogUrl\":")
   article_urls = []
   for line in output:
     article= re.search('http:.*.aljazeera.*.html","ogType":"article"',line)
     try:
       a = article.group(0).strip('","ogType":"article"')
       article_urls.append(a+"l")
     except:
       pass
   top_articles = []
   for url in article_urls[0:news_interface.NUM_ARTICLES]:
     top_articles.append(self.get_article(url))
