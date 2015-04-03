from bs4 import BeautifulSoup
import news_interface
import news_orgs


class GlobeAndMail(news_interface.NewsOrg):
  '''Methods for interacting with the Globe and Mail website.'''

  def __init__(self):
    self.news_org = news_orgs.GLOBE_AND_MAIL
    self.search_url = 'http://www.theglobeandmail.com/search/?q=%s'

  def __repr__(self):
    return self.news_org

  def get_headline(self, soup):
    soup.h1.a.extract()
    headline = soup.h1.get_text().encode('ascii', 'ignore').strip('\n')
    return headline

  def get_body(self, soup):
    article = soup.find('div', attrs={'class': 'entry-content'})

    # Remove other content that is inline with the article text
    [div.extract() for div in
        article.find_all('div', attrs={'class': 'entry-related'})]
    [aside.extract() for aside in article.find_all('aside')]

    paragraphs = article.find_all('p', attrs={'class': None})
    body = ' '.join(
        [p.get_text().encode('ascii', 'ignore') for p in paragraphs])
    return body

  def get_date(self, soup):
    date = soup.find('time').string
    return date

  def process_search_results(self, res):
    soup = BeautifulSoup(res.text)
    articles = soup.find_all('h3')
    root = 'http://www.theglobeandmail.com'
    article_urls = [root + article.a.get('href') for article in articles
        if article.a]
    non_video_urls = [url for url in article_urls if 'news-video' not in url]
    return non_video_urls
