# -*- coding: utf-8 -*-
import nltk
from nltk.corpus import wordnet as wn
from nltk.chunk.regexp import *

import logger


DefaultNpPattern = ''.join([r'(<DT|AT>?<RB>?)?',
			    r'<JJ.*|CD.*>*',
			    r'(<JJ.*|CD.*><,>)*',
			    r'(<N.*>)+'])
BaselineNpChunkRule = ChunkRule(DefaultNpPattern,
                                'Default rule for NP chunking')
NpChunker = RegexpChunkParser([BaselineNpChunkRule])

DISTANCE_LIMIT = 6


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

def get_phrases(string, org):
  '''Returns the noun and verb phrases in string.

  Args:
    string: A string.
    org: The NewsOrg that wrote the string.

  Returns:
    A tuple of two dictionaries: one of the noun phrases in string to the
    sentence in string that it came from, and similarly for verb phrases.
  '''
  NPs = {}
  VPs = {}
  for sentence in string.split('.'):
    tokens = nltk.word_tokenize(sentence)
    #logger.log.info('Tokens from %s: %s' % (org, tokens))
    tagged_tokens = nltk.pos_tag(tokens)
    for word, tag in tagged_tokens:
      word = lemmatize(word, 'v')
      if tag.startswith('V') and word in VPs.keys():
        VPs[word].append(sentence)
      else:
        VPs[word] = [sentence]
    for np in chunk(tagged_tokens):
      if np in NPs.keys():
        NPs[np].append(sentence)
      else:
        NPs[np] = [sentence]
  return NPs, VPs

def chunk(pos_tagged_tokens):
  chunks = []
  tree = NpChunker.parse(pos_tagged_tokens)
  for child in tree:
    if type(child) == nltk.Tree and child.label() == 'NP':
      leaves = child.leaves()
      chunks.append(leaves_to_str(check_wn_phrase(leaves)))

  return chunks

def get_synset(np):
  tokens = nltk.word_tokenize(np)
  try:
    synsets = wn.synsets('_'.join(tokens), 'n')
  except:
    return None

  while tokens and not synsets:
    # remove modifiers from noun head
    tagged_np = nltk.pos_tag(tokens)
    if not tagged_np[0][1].startswith('NN'):
      tokens = tokens[1:]
    else:
      break
    try:
      synsets = wn.synsets('_'.join(tokens), 'n')
    except:
      return None

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

def synset_distance(hypo, hyper, acc=0):
  #logger.log.info('Hypo: %s' % (hypo))
  if acc == DISTANCE_LIMIT:
    return acc
  if hypo in hyper:
    return 0
  hypernyms = hypo.hypernyms()
  if not hypernyms:
    return float("inf")
  return 1 + min([synset_distance(new_hypo, hyper, acc + 1) for new_hypo in hypernyms])

def get_ancestors(synset):
  try:
    ancestors = synset.hypernyms()
  except:
    return []
  for hypernym in synset.hypernyms():
    ancestors.extend(get_ancestors(hypernym))
  return ancestors

def get_synsets_and_ancestors(phrases, NP=True):
  '''Returns a list of synsets in phrases, and their ancestors.

  Args:
    phrases: A list of phrases (NPs or VPs).

  Returns:
    A list of the synsets contained in phrases, and their ancestors.
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

  return [(synset.pos(), synset.offset()) for synset in synsets]

def highlight_sentence(highlighted_sentences, phrases, key):
  sentence = phrases[key][0].encode('utf-8').strip() + '.'
  if sentence in highlighted_sentences:
    highlighted_sentences[sentence] = highlighted_sentences[sentence].replace(
                                        key, '**%s**' % key)
  else:
    highlighted_sentences[sentence] = sentence.replace(key, '**%s**' % key)
  return highlighted_sentences

def check_distances(diff, comparison_synsets, phrase_to_sentence,
                    highlighted_sentences, NP=True):
  '''Checks the distance from each NP in diff to the comparison_synsets and
  adds the corresponsing sentence from NP_to_sentence to highlighted_sentences
  if the distance is great enough.

  diff: A list of noun or verb phrases.
  comparison_synsets: A list of noun or verb synsets.
  phrase_to_sentence: An NP or VP to sentence dictionary.
  highlighted_sentences: A dict of sentences to their highlighted versions.
  NP: True if the phrases are noun phrases, False if they are verb phrases.

  Returns: None, but alters highlighted_sentences.
  '''
  for phrase in diff:
    phrase = phrase.encode('utf-8')
    try:
      if NP:
        synset = get_synset(phrase)
      else:
        synset = wn.synsets(phrase, 'v')
        if synset:
          synset = synset[0]
    except:
      return float('inf')

    if synset:
      distance = synset_distance(synset, comparison_synsets)
      if distance >= DISTANCE_LIMIT and distance != float("inf"):
        highlight_sentence(highlighted_sentences, phrase_to_sentence, phrase)

def compare_articles(a1_NP_to_sentence, a1_VP_to_sentence,
                     a1_NPs, a1_VPs,
                     a1_NP_synsets, a1_VP_synsets,
                     comparison_article):
  '''Compares the noun and verb phrases of article a1 to a comparison_article.

  Args:
    a1_NP_to_sentence: A dict of each noun phrase in article 1 to the sentence
      that contains it.
    a1_VP_to_sentence: A dict of each verb phrase in article 1 to the sentence
      that contains it.
    a1_NPs: A list of every noun phrase in article 1.
    a1_VPs: A list of every verb phrase in article 1.
    a1_NP_synsets: A list of all the noun synsets and their ancestors from
      article 1.
    a1_VP_synsets: A list of all the verb synsets and their ancestors from
      article 1.
    comparison_article: the Article to be compared to article 1.

  Returns:
    A dictionary representation of comparison_article, including a list of
    sentences that contain semantic concepts very different from the article a1.
  '''
  a2_NP_to_sentence, a2_VP_to_sentence = get_phrases(
      comparison_article.body, comparison_article.news_org)

  a2_NPs = set(a2_NP_to_sentence)
  a2_VPs = set(a2_VP_to_sentence)

  diff_NPs = a2_NPs.difference(a1_NPs)
  diff_VPs = a2_VPs.difference(a1_VPs)

  highlighted_sentences = {}
  check_distances(diff_NPs, a1_NP_synsets, a2_NP_to_sentence,
                  highlighted_sentences)
  check_distances(diff_VPs, a1_VP_synsets, a2_VP_to_sentence,
                  highlighted_sentences, NP=False)

  comparison_results = comparison_article.to_dict()
  comparison_results['sentences'] = highlighted_sentences.values()
  if comparison_results['sentences']:
    return comparison_results
  else:
    return None

def compare_to_all_articles(article, comparison_articles):
  '''Compares article to the comparison_articles.
  TODO: Deprecate this in favour of parallel comparisons.

  Args:
    article: an Article
    comparison_articles: a list of Articles to be compared to the article_body

  Returns:
    The list of comparison_articles in JSON format, with a 'sentences'
    attribute containing a list of sentences with different facts from the
    original article.
  '''
  articleNPs, articleVPs = get_phrases(article.body, article.news_org)

  NPs = set(articleNPs.keys())
  NP_synsets = get_synsets_and_ancestors(articleNPs)

  VPs = set(articleVPs.keys())
  VP_synsets = get_synsets_and_ancestors(articleVPs, NP=False)

  all_results = []
  for comparison_article in comparison_articles:
    if comparison_article:
      comparison_results = comparison_article.to_dict()
      comparison_results = compare_articles(
          articleNPs, articleVPs, NPs, VPs, NP_synsets, VP_synsets,
          comparison_article)
      all_results.append(comparison_results)
  return all_results
