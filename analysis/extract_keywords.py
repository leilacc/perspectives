'''Extracts key words from a news article headline.'''

import nltk

STOPWORDS = nltk.corpus.stopwords.words('english')
# Used when tokenizing words
SENTENCE_RE = r'''
    (?x)                    # set flag to allow verbose regexps
    ([A-Z])(\.[A-Z])+\.?    # abbreviations, e.g. U.S.A.
    | \w+(-\w+)*            # words with optional internal hyphens
    | \$?\d+(\.\d+)?%?      # currency and percentages, e.g. $12.40, 82%
    | \.\.\.                # ellipsis
    | [][.,;"'?():-_`]      # these are separate tokens
'''


def remove_stopwords(sentence):
  '''Removes the stopwords from a sentence.

  sentence: A string.

  Returns: sentence, unchanged except for having stopwords removed.
  '''
  content_words = []
  for word in sentence.split():
    if word not in STOPWORDS:
      content_words.append(word)
  return ' '.join(content_words)

def extract_keywords(headline):
  '''Extracts key words from a news article headline.

  headline: A string.

  Returns: A string of keywords extracted from headline.
  '''
  headline = headline.lower()
  content_headline = remove_stopwords(headline)
  tokens = nltk.regexp_tokenize(content_headline, SENTENCE_RE)
  pos_tokens = nltk.tag.pos_tag(tokens)

  keywords = []
  for (word, tag) in pos_tokens:
    if tag == "NN":
      keywords.append(word)

  return ' '.join(keywords)
