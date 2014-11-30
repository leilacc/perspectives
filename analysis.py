# -*- coding: utf-8 -*-
import json
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
  return NPleaves

def get_NPs(sentence):
  tokens = nltk.word_tokenize(sentence)
  tagged_tokens = nltk.pos_tag(tokens)
  NPs = chunk(tagged_tokens)
  return NPs

def chunk(pos_tagged_tokens):
  chunks = []
  tree = NpChunker.parse(pos_tagged_tokens)
  for child in tree:
    if type(child) == nltk.Tree and child.node == 'NP':
      leaves = child.leaves()
      chunks.append(leaves_to_str(check_wn_phrase(leaves)))

  return chunks

def get_synsets(np):
  tokens = nltk.word_tokenize(np)
  synsets = wn.synsets('_'.join(tokens))
  while np and not synsets:
    # remove modifiers from noun head
    tagged_np = nltk.pos_tag(tokens)
    if not tagged_np[0][1].startswith('NN'):
      tokens = tokens[1:]
    else:
      break
    synsets = wn.synsets('_'.join(tokens))

  return synsets

def syn(np1, np2):
  max_lch = 0
  max_syns = ()
  syn1 = get_synsets(np1)[0]
  syn2 = get_synsets(np2)[0]
  try:
    if syn1 != syn2:
      lch = syn1.lch_similarity(syn2)
      if lch > max_lch:
        max_syns = (syn1, syn2)
        max_lch = lch
  except:
    pass
  if max_lch > 1.6:
    return max_syns

def get_NP_syns(article1_NPs, article2_NPs):
  syns = []
  for np1 in article1_NPs:
    for np2 in article2_NPs:
      if np1 in LOADED_WORDS and np2 in LOADED_WORDS:
        syn_match = syn(np1, np2)
        if syn_match:
          syns.append(syn_match)

  return syns


if __name__ == '__main__':
  with open('article1.json') as article1:
    article1 = json.load(article1)
    article1_NPs = set(get_NPs(article1["title"]) + get_NPs(article1["article_text"]))

    with open('article2.json') as article2:
      article2 = json.load(article2)
      article2_NPs = set(get_NPs(article2["title"]) + get_NPs(article2["article_text"]))
      print get_NP_syns(article1_NPs, article2_NPs)
