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

def get_synset(np):
  tokens = nltk.word_tokenize(np)
  synsets = wn.synsets('_'.join(tokens), 'n')
  while tokens and not synsets:
    # remove modifiers from noun head
    tagged_np = nltk.pos_tag(tokens)
    if not tagged_np[0][1].startswith('NN'):
      tokens = tokens[1:]
    else:
      break
    synsets = wn.synsets('_'.join(tokens), 'n')

  if synsets:
    return synsets[0]

def get_definition_synsets(definition):
  tokens = nltk.word_tokenize(definition)
  tagged_tokens = nltk.pos_tag(tokens)
  synsets = []
  for token, tag in tagged_tokens:
    if tag.startswith('NN'):
      synset = get_synset(token)
      if synset and synset.min_depth > 3:
        synsets.append(synset)
  return synsets

def get_synsets(np1, np2):
  max_lch = 0
  max_syns = ()
  syn1 = get_synset(np1)
  if syn1:
    synsets1 = [syn1] + get_definition_synsets(syn1.definition)
  syn2 = get_synset(np2)
  if syn2:
    synsets2 = [syn2] + get_definition_synsets(syn2.definition)

  if not syn1 or not syn2:
    return
  return (synsets1, synsets2)

def determine_if_related(np1, np2):
  syn1 = get_synset(np1)
  syn2 = get_synset(np2)

  if syn1 and syn2 and syn1.max_depth() > 5 and syn2.max_depth() > 5:
    lch = syn1.lowest_common_hypernyms(syn2)[0]
    if lch not in [syn1, syn2] and synset_distance(syn1, lch) + synset_distance(syn2, lch) < 5:
      return (syn1, syn2)

def synset_distance(hypo, hyper):
  if hypo == hyper:
    return 0
  hypernyms = hypo.hypernyms()
  if not hypernyms:
    return float("inf")
  return 1 + min([synset_distance(new_hypo, hyper) for new_hypo in hypernyms])

def get_NP_syns(article1_NPs, article2_NPs):
  syns = []
  for np1 in article1_NPs:
    for np2 in article2_NPs:
      if ((np1 in LOADED_WORDS) ^ (np2 in LOADED_WORDS)):
        syn_match = determine_if_related(np1, np2)
        if syn_match:
          syns.append((np1, np2))

  return syns


if __name__ == '__main__':
  with open('article1.json') as article1:
    article1 = json.load(article1)
    article1_NPs = set(get_NPs(article1["title"]) + get_NPs(article1["article_text"]))

    with open('article2.json') as article2:
      article2 = json.load(article2)
      article2_NPs = set(get_NPs(article2["title"]) + get_NPs(article2["article_text"]))
      article2_NPs = article2_NPs.difference(article1_NPs)
      print get_NP_syns(article1_NPs, article2_NPs)
