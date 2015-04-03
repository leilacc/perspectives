import json

import api_keys
import news_interface
import news_orgs


class HuffPost(news_interface.NewsOrg):
  '''Methods for interacting with the Huffington Post website/API.'''

  def __init__(self):
    self.news_org = news_orgs.HUFF_POST
    self.search_url = ('https://www.googleapis.com/customsearch/v1element?key='
        + api_keys.api_keys[news_orgs.HUFF_POST] +
        '&rsz=10&num=10&hl=en&prettyPrint=false&source=gcsc&gss=.com&sig=23952f'
        '7483f1bca4119a89c020d13def&cx=004830092955692134028:an6per91wyc&q=%s&a'
        's_sitesearch=huffingtonpost.com&googlehost=www.google.com&callback=goo'
        'gle.search.Search.apiary17234&nocache=1422138917068')

  def __repr__(self):
    return self.news_org

  def get_headline(self, soup):
    headline = soup.h1.string
    return headline

  def get_body(self, soup):
    article = soup.find('article', attrs={'class': 'entry'})
    paragraphs = article.find_all('p', attrs={'class': None})
    body = ' '.join([p.get_text() for p in paragraphs])
    return body

  def get_date(self, soup):
    date = soup.find('span', attrs={'class': 'posted'}).find('time').string
    return date

  def process_search_results(self, res):
    results = json.loads(res.text[49:-2])['results']
    article_urls = [res['url'] for res in results]
    # Huff Post sometimes returns aggregator pages that don't
    # contain an article and don't end in .html
    article_urls = [url for url in article_urls if url.endswith('html')]
    return article_urls

