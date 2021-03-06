'''Get perspectives from different articles.'''

import futures
import json
import re
import urllib

from nltk.corpus import wordnet as wn

import compare_articles
import extract_keywords
from scraping import aljazeera, bbc, cbc, cnn, globe_and_mail, guardian, \
                     huff_post, jpost, ny_post, ny_times, reuters, \
                     russia_today, times_of_israel, todays_zaman, usa_today
from scraping import logger

AL_JAZEERA = aljazeera.AlJazeera()
BBC = bbc.BBC()
CBC = cbc.CBC()
CNN = cnn.CNN()
GLOBE_AND_MAIL = globe_and_mail.GlobeAndMail()
GUARDIAN = guardian.Guardian()
HUFF_POST = huff_post.HuffPost()
JPOST = jpost.JPost()
NY_POST = ny_post.NYPost()
NY_TIMES = ny_times.NYTimes()
REUTERS = reuters.Reuters()
RT = russia_today.RussiaToday()
TIMES_OF_ISRAEL = times_of_israel.TimesOfIsrael()
TODAYS_ZAMAN = todays_zaman.TodaysZaman()
USA_TODAY = usa_today.USAToday()

NEWS_ORGS = [AL_JAZEERA, BBC, CBC, CNN, GLOBE_AND_MAIL, GUARDIAN, HUFF_POST,
             JPOST, NY_POST, NY_TIMES, REUTERS, RT, TIMES_OF_ISRAEL,
             TODAYS_ZAMAN, USA_TODAY]

def get_article_phrases(body, org):
  NP_to_sentence, VP_to_sentence = compare_articles.get_phrases(body, org)
  NPs = set(NP_to_sentence.keys())
  VPs = set(VP_to_sentence.keys())
  NP_synsets = compare_articles.get_synsets_and_ancestors(NPs)
  VP_synsets = compare_articles.get_synsets_and_ancestors(VPs, NP=False)
  return (NP_to_sentence, VP_to_sentence, NPs, VPs, NP_synsets, VP_synsets)

def urldecode(url):
  '''Decode URLencoded url.'''
  return urllib.unquote(url).decode('utf8')

def get_perspectives(url):
  '''Get different perspectives on the topic covered by article.

  Args:
    url: A URLencoded string.

  Returns:
    A JSON-encoded string representing other articles with different
    perspectives than the original article.

    Format: a list of Article.to_dict()s, each with an additional 'sentences'
    attribute. 'sentences' contains a list of sentences with semantically
    different words that were extracted from the corresponding article's body.
  '''
  article = url_to_article(urldecode(url))
  if article:
    headline = article.headline
    body = article.body
    org = article.news_org

    article_topic = extract_keywords.extract_keywords(headline)

    (NP_to_sentence, VP_to_sentence, NPs, VPs, NP_synsets, VP_synsets) = \
        get_article_phrases(body, org)

    n = len(NEWS_ORGS)
    with futures.ProcessPoolExecutor(max_workers=n) as executor:
      comparisons = executor.map(get_comparison, NEWS_ORGS,
                                 [NP_to_sentence]*n, [VP_to_sentence]*n,
                                 [NPs]*n, [VPs]*n,
                                 [NP_synsets]*n, [VP_synsets]*n,
                                 [article_topic]*n, [headline]*n, [org]*n)
      compared_articles_by_org = list(comparisons)
      # flatten from list of lists of articles (separated by news org) to list
      # of articles
      compared_articles = [article for org_articles in compared_articles_by_org
                           for article in org_articles if article]
      return json.dumps(compared_articles)
  else:
    return json.dumps({"Error": "Not a recognized article"})

def get_comparison(news_org, NP_to_sentence, VP_to_sentence,
                   NPs, VPs, NP_synsets, VP_synsets,
                   article_topic, article_headline, article_news_org):
  '''Compares the articles from a single NewsOrg to an article that is
  represented by its NPs and VPs.'''
  # synsets aren't picklable so they're stored as (pos, offset) and unpacked
  NP_synsets = [wn._synset_from_pos_and_offset(pos, offset)
                for (pos, offset) in NP_synsets]
  VP_synsets = [wn._synset_from_pos_and_offset(pos, offset)
                for (pos, offset) in VP_synsets]

  comparison_articles = news_org.get_query_results(article_topic)
  if not comparison_articles:
    logger.log.warning("No comparison articles for %s" % news_org)
    return []
  comparisons = []
  for comparison_article in comparison_articles:
    if (news_org == article_news_org and
        comparison_article.headline == article_headline):
      # comparison_article is likely the same as the original article
      # do not compare
      pass
    try:
      comparison = compare_articles.compare_articles(NP_to_sentence,
                                                     VP_to_sentence, NPs, VPs,
                                                     NP_synsets, VP_synsets,
                                                     comparison_article)
      if comparison:
        comparisons.append(comparison)
    except:
      continue
  return comparisons

def url_to_article(url):
  '''Returns the Article at url if the url is supported.

  Args:
    url: A string.

  Returns:
    The Article that is scraped from url, if the url corresponds to an article
    on a supported news org page. Otherwise, None.
  '''
  if re.search(r'.*aljazeera\.com/((opinions)|(articles)|(news))/.+', url):
    return AL_JAZEERA.get_article(url)
  elif re.search(r'.*bbc\..+', url):
    return BBC.get_article(url)
  elif re.search(r'.*cbc\.ca/news/.+', url):
    return CBC.get_article(url)
  elif re.search(r'.*cnn\.com/.+', url):
    return CNN.get_article(url)
  elif re.search(r'.*theglobeandmail\.com/.+', url):
    return GLOBE_AND_MAIL.get_article(url)
  elif re.search(r'.*theguardian\.com/.+', url):
    return GUARDIAN.get_article(url)
  elif re.search(r'.*huffingtonpost\.c.+/.+', url):
    return HUFF_POST.get_article(url)
  elif re.search(r'.*jpost\.com/.+', url):
    return JPOST.get_article(url)
  elif re.search(r'.*nypost\.com/.+', url):
    return NY_POST.get_article(url)
  elif re.search(r'.*nytimes\.com/.+', url):
    return NY_TIMES.get_article(url)
  elif re.search(r'.*reuters\.com/.+', url):
    return REUTERS.get_article(url)
  elif re.search(r'.*rt\.com/.+', url):
    return RT.get_article(url)
  elif re.search(r'.*timesofisrael\.com/.+', url):
    return TIMES_OF_ISRAEL.get_article(url)
  elif re.search(r'.*todayszaman\.com/.+', url):
    return TODAYS_ZAMAN.get_article(url)
  elif re.search(r'.*usatoday\.com/story/.+', url):
    return USA_TODAY.get_article(url)
  else:
    logger.log.info("Didn't regexp match for %s" % url)
    return None
