# -*- coding: utf-8 -*-
import nltk
from nltk.corpus import wordnet as wn
from nltk.chunk.regexp import *


DefaultNpPattern = ''.join([r'(<DT|AT>?<RB>?)?',
			    r'<JJ.*|CD.*>*',
			    r'(<JJ.*|CD.*><,>)*',
			    r'(<N.*>)+'])
BaselineNpChunkRule = ChunkRule(DefaultNpPattern,
                                'Default rule for NP chunking')
NpChunker = RegexpChunkParser([BaselineNpChunkRule],
                              chunk_node='NP',top_node='S')

with open('loaded_words.txt', 'r') as f:
  LOADED_WORDS = [line.strip('\n').lower()
                  for line in f
                  if not line.startswith('#')]

def lemmatize(word, pos):
  # lemmatizes a word
  return nltk.stem.WordNetLemmatizer().lemmatize(word, pos)

def leaves_to_str(NPleaves):
  # converts leaves to strings
  leaf_strs = []
  for leaf in NPleaves:
    leaf_strs.append(lemmatize(leaf[0], 'n'))
  return ' '.join(leaf_strs)

def form_wn_phrase(NPleaves):
  # Generate a string of words in the NPleaves joined by underscores
  # which can be used to check if the phrase has any synsets in WN
  phrase = []
  for leaf in NPleaves:
    phrase.append(leaf[0])
  print phrase
  return '_'.join(phrase)

def check_wn_phrase(NPleaves):
  # check if the words in NPleaves form a common phrase according to WN
  while NPleaves[0][1] == 'DT':
    # remove determiners
    NPleaves = NPleaves[1:]

  while ((NPleaves[0][1].startswith('CD') or
          NPleaves[0][1].startswith('RB') or
          NPleaves[0][1].startswith('JJ')) and
         not wn.synsets(form_wn_phrase(NPleaves) ,'n')):
    # remove leading numbers,adverbs, and adjectives that do not form a
    # commonly-used phrase according to WN
    NPleaves = NPleaves[1:]
  print NPleaves
  return NPleaves

def get_NPs(sentence):
  tokens = nltk.word_tokenize(sentence)
  tagged_tokens = nltk.pos_tag(tokens)
  NPs = chunk(tagged_tokens)

def chunk(pos_tagged_tokens):
  chunks = []
  cur_chunk = []
  tree = NpChunker.parse(pos_tagged_tokens)
  for child in tree:
    if type(child) == nltk.Tree and child.node == 'NP':
      leaves = child.leaves()
      print leaves
      cur_chunk.append(leaves_to_str(check_wn_phrase(leaves)))
  if cur_chunk:
    # catch the last chunk
    chunks.append(''.join(cur_chunk))

  return chunks

def syn(word1, word2):
  max_lch = 0
  max_syns = ()
  for syn1 in wn.synsets(word1):
    for syn2 in wn.synsets(word2):
      try:
        lch = syn1.lch_similarity(syn2)
        if lch > max_lch:
          max_syns = (syn1, syn2)
          max_lch = lch
      except:
        continue
  if max_lch > 1.5:
    return max_syns

def compare_NPs(article1, article2):
  set(get_NPs(article.headline) + get_NPs(article.text))



if __name__ == '__main__':
  print get_NPs('ICC finds Israel guilty of war crimes in Mavi Marmara raid')
