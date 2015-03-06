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
NpChunker = RegexpChunkParser([BaselineNpChunkRule])

def lemmatize(word, pos):
  # lemmatizes a word
  return nltk.stem.WordNetLemmatizer().lemmatize(word, pos)

def leaves_to_str(NPleaves):
  # converts leaves to strings
  leaf_strs = []
  for leaf in NPleaves:
    leaf_strs.append(leaf[0])
  return ' '.join(leaf_strs)

def form_wn_phrase(NPleaves):
  # Generate a string of words in the NPleaves joined by underscores
  # which can be used to check if the phrase has any synsets in WN
  phrase = []
  for leaf in NPleaves:
    phrase.append(leaf[0])
  return '_'.join(phrase)

def check_wn_phrase(NPleaves):
  for leaf in NPleaves:
    leaf = (lemmatize(leaf[0], 'n'), leaf[1])

  # check if the words in NPleaves form a common phrase according to WN
  while NPleaves[0][1] == 'DT':
    # remove determiners
    NPleaves = NPleaves[1:]

  while ((not NPleaves[0][1].startswith('NN')) and
         not wn.synsets(form_wn_phrase(NPleaves) ,'n')):
    # remove leading numbers,adverbs, and adjectives that do not form a
    # commonly-used phrase according to WN
    NPleaves = NPleaves[1:]
  while ((not NPleaves[-1][1].startswith('NN')) and
         not wn.synsets(form_wn_phrase(NPleaves) ,'n')):
    # remove leading numbers,adverbs, and adjectives that do not form a
    # commonly-used phrase according to WN
    NPleaves = NPleaves[0:-1]
  return NPleaves

def get_VPs(string):
  VPs = {}
  for sentence in string.split('.'):
    tokens = nltk.word_tokenize(sentence)
    tagged_tokens = nltk.pos_tag(tokens)
    for word, tag in tagged_tokens:
      word = lemmatize(word, 'v')
      if tag.startswith('V') and word in VPs.iterkeys():
        VPs[word].append(sentence)
      else:
        VPs[word] = [sentence]
  return VPs

def get_NPs(string):
  NPs = {}
  for sentence in string.split('.'):
    tokens = nltk.word_tokenize(sentence)
    tagged_tokens = nltk.pos_tag(tokens)
    for np in chunk(tagged_tokens):
      if np in NPs.iterkeys():
        NPs[np].append(sentence)
      else:
        NPs[np] = [sentence]
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

def synset_distance(hypo, hyper):
  if hypo in hyper:
    return 0
  hypernyms = hypo.hypernyms()
  if not hypernyms:
    return float("inf")
  return 1 + min([synset_distance(new_hypo, hyper) for new_hypo in hypernyms])

def get_ancestors(synset):
  ancestors = synset.hypernyms()
  for hypernym in synset.hypernyms():
    ancestors.extend(get_ancestors(hypernym))
  return ancestors

def get_synsets_and_ancestors(phrases, NP=True):
  '''Returns a list of synsets in phrases, and their ancestors.

  phrases: A list of phrases (NPs or VPs).
  '''
  synsets = []
  for phrase in phrases:
    if phrase:
      synset = get_synset(phrase)
    else:
      synset = wn.synsets(phrase, 'v')

    if synset:
      synsets.append(synset)
      synsets.extend(get_ancestors(synset))

  return synsets

def highlight_sentence(highlighted_sentences, phrases, key):
  sentence = phrases[key][0].encode('utf-8').strip() + '.'
  if sentence in highlighted_sentences:
    highlighted_sentences[sentence] = highlighted_sentences[sentence].replace(
                                        key, '**%s**' % key)
  else:
    highlighted_sentences[sentence] = sentence.replace(key, '**%s**' % key)
  return highlighted_sentences

def compare_articles(a1_NPs, a1_VPs, a1_NP_synsets, a1_VP_synsets,
                     NPs, VPs, a2_text):
  '''Returns a list of sentences from article2 that contain semantic concepts
  very different from article1.'''
  a2_NP_to_sentence = get_NPs(a2_text)
  a2_VP_to_sentence = get_VPs(a2_text)

  a2_NPs = set(a2_NP_to_sentence)
  a2_VPs = set(a2_VP_to_sentence)

  diff_NPs = a2_NPs.difference(a1_NPs)
  diff_VPs = a2_VPs.difference(a1_VPs)

  highlighted_sentences = {}
  for np in diff_NPs:
    np = np.encode('utf-8')
    synset = get_synset(np)
    if synset:
      distance = synset_distance(synset, a1_NP_synsets)
      if distance > 3:
        highlight_sentence(highlighted_sentences, a2_NP_to_sentence, np)

  for verb in diff_VPs:
    verb = verb.encode('utf-8')
    synset = wn.synsets(verb, 'v')
    if synset:
      synset = synset[0]
      distance = synset_distance(synset, a1_VP_synsets)
      if distance > 5 and distance != float("inf"):
        highlight_sentence(highlighted_sentences, a2_VP_to_sentence, verb)

  return highlighted_sentences.values()

def compare_to_all_articles(article_body, comparison_articles):
  '''Compares article to the comparison_articles.
  TODO: Deprecate this in favour of parallel comparisons.

  Args:
    article_body: string, the body of an Article
    comparison_articles: a list of Articles to be compared to the article_body

  Returns:
    The list of comparison_articles in JSON format, with a 'sentences'
    attribute containing a list of sentences with different facts from the
    original article.
  '''
  articleNPs = get_NPs(article_body)
  NPs = set(articleNPs.keys())
  NP_synsets = get_synsets_and_ancestors(articleNPs)

  articleVPs = get_VPs(article_body)
  VPs = set(articleVPs.keys())
  VP_synsets = get_synsets_and_ancestors(articleVPs, NP=False)

  all_results = []
  for comparison_article in comparison_articles:
    if comparison_article:
      comparison_results = comparison_article.to_dict()
      comparison_results['sentences'] = compare_articles(
          articleNPs, articleVPs, NPs, VPs, NP_synsets, VP_synsets,
          comparison_article.body)
      all_results.append(comparison_results)
  return json.dumps(all_results)
