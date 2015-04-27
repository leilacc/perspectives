import helpers
import news_interface
import news_orgs


class TimesOfIsrael(news_interface.NewsOrg):
  '''Methods for interacting with the Times of Israel website.'''

  def __init__(self):
    self.news_org = news_orgs.TIMES_OF_ISRAEL
    self.search_url = "https://www.googleapis.com/customsearch/v1element?key=AIzaSyCVAXiUzRYsML1Pv6RwSG1gunmMikTzQqY&rsz=filtered_cse&num=10&hl=en&prettyPrint=false&source=gcsc&gss=.com&sig=23952f7483f1bca4119a89c020d13def&cx=015742192883069867459:k3m1yn-i4ua&q=%s&googlehost=www.google.com&callback=google.search.Search.apiary782&nocache=1422549552720"

  def __repr__(self):
    return self.news_org

  def get_headline(self, soup):
    h1 = soup.find('h1', attrs={'class': 'headline'})
    headline = h1.text
    return headline

  def get_body(self, soup):
    paragraphs = soup.findAll("p", {"itemprop": "articleBody"})
    body = ' '.join([helpers.decode(p.text) for p in paragraphs])
    return body

  def get_date(self, soup):
    date = soup.find('span', attrs={'class': 'date'}).getText()
    return date

  def process_search_results(self, res):
    output = res.text.encode('ascii', 'ignore').split("\"ogUrl\":")
    article_urls = []
    for line in output:
      try:
        a = line.split(",")[0].replace('"',"")
        if "http" in a:
          article_urls.append(a)
      except:
        pass
    return article_urls
