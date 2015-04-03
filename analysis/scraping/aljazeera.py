import json
import logger
import news_interface
import news_orgs


class AlJazeera(news_interface.NewsOrg):
  '''Methods for interacting with the Al Jazeera website.'''

  def __init__(self):
    self.news_org = news_orgs.ALJAZEERA
    self.search_url = ("https://www.googleapis.com/customsearch/v1element?key" +
                       "=AIzaSyCVAXiUzRYsML1Pv6RwSG1gunmMikTzQqY&rsz=filtered" +
                       "_cse&num=10&hl=en&prettyPrint=false&source=gcsc&gss=." +
                       "com&sig=23952f7483f1bca4119a89c020d13def&cx=007864276" +
                       "874919660377:szp4pg3raxu&q=%s&lr=lang_en&filter=1&sor" +
                       "t=&googlehost=www.google.com&callback=google.search.S" +
                       "earch.apiary7638&nocache=1422548009762")

  def __repr__(self):
    return self.news_org

  def get_headline(self, soup):
    '''Implementation of get_headline.'''
    headline = None
    potential_classes = ["heading-story", "articleOpinion-title"]
    for h1_class in potential_classes:
      try:
        headline = soup.find("h1", {"class": h1_class}).string
        break
      except AttributeError:
        continue
    if not headline:
      logger.log.error(
          'Exception trying to scrape Al Jazeera headline from %s' % (url))
      return None
    return headline

  def get_body(self, soup):
    try:
      paragraphs = soup.find("div", {"class": "article-body"})
      article = paragraphs.findAll("p")
    except AttributeError:
      paragraphs = soup.find("div", {"class": "text"})
      article = paragraphs.findAll("p")
    body = ' '.join([p.text for p in article])
    return body

  def get_date(self, soup):
    try:
      date = soup.find("time").string
    except AttributeError:
      date = soup.find("span", {"class": "date"}).string
    return date

  def process_search_results(self, raw_results):
    json_res = raw_results.text.encode('ascii', 'ignore')[48:-2]
    json_res = json.loads(json_res)['results']
    article_urls = [result['url'] for result in json_res]
    # Remove urls that don't link to articles
    article_urls = [url for url in article_urls
                    if 'topics' not in url and 'blogs' not in url]
    return article_urls
