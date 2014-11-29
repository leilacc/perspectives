import nltk
from nltk.corpus import wordnet as wn
from nltk.chunk.regexp import *

with open('loaded_words.txt', 'r') as f:
  LOADED_WORDS = [line.strip('\n').lower()
                  for line in f
                  if not line.startswith('#')]

print LOADED_WORDS

def lemmatize(word, pos):
  # lemmatizes a word
  return nltk.stem.WordNetLemmatizer().lemmatize(word, pos)

def analyze(headline, text):
  BaselineNpChunkRule = ChunkRule(DefaultNpPattern,
                                  'Default rule for NP chunking')
  NpChunker = RegexpChunkParser([BaselineNpChunkRule],
                                chunk_node='NP',top_node='S')
  tree = NpChunker.parse(nltk.pos_tag(nltk.word_tokenize(prediction_question)))
  print tree

def syn(word1, word2, lch_threshold=1.8):
  for net1 in wn.synsets(word1):
    for net2 in wn.synsets(word2):
      try:
        lch = net1.lch_similarity(net2)
      except:
        continue
      # The value to compare the LCH to was found empirically.
      # (The value is very application dependent. Experiment!)
      print "%s %s %f" % (net1, net2, lch)
      if lch >= lch_threshold:
        yield (net1, net2, lch)
