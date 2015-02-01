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

def determine_if_related(np1, np2):
  syn1 = get_synset(np1)
  syn2 = get_synset(np2)

  if syn1 and syn2 and syn1.max_depth() > 5 and syn2.max_depth() > 5:
    lch = syn1.lowest_common_hypernyms(syn2)[0]
    if lch not in [syn1, syn2] and synset_distance(syn1, [lch]) + synset_distance(syn2, [lch]) < 5:
      return (syn1, syn2)

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

def get_sentence(np, string):
  matching_sentences = []
  for sentence in string.split('.'):
    tokens = nltk.word_tokenize(sentence)
    tagged_tokens = nltk.pos_tag(tokens)
    tree = NpChunker.parse(tagged_tokens)
    for child in tree:
      if type(child) == nltk.Tree and child.node == 'NP':
        leaves = child.leaves()
        if np in ' '.join([lemmatize(leaf[0], 'n') for leaf in leaves]):
          matching_sentences.append(sentence)
  return matching_sentences

def get_tree(sentence):
    tokens = nltk.word_tokenize(sentence)
    tagged_tokens = nltk.pos_tag(tokens)
    return NpChunker.parse(tagged_tokens)

def compare_articles(article1, article2):
    text_NPs = get_NPs(article1.body)
    article1_NPs = set(text_NPs.keys())
    text_VPs = get_VPs(article1.body)
    article1_VPs = set(text_VPs.keys())

    text_NPs = get_NPs(article2.body)
    article2_NPs = set(text_NPs.keys())
    diff_NPs = article2_NPs.difference(article1_NPs)
    text_VPs = get_VPs(article2.body)
    article2_VPs = set(text_VPs.keys())
    diff_VPs = article2_VPs.difference(article1_VPs)

    syns1 = []
    for np in article1_NPs:
      synset = get_synset(np)
      if synset:
        syns1.append(synset)
        syns1.extend(get_ancestors(synset))

    sentences = {}
    for np in diff_NPs:
      np = np.encode('utf-8')
      synset = get_synset(np)
      if synset:
        distance = synset_distance(synset, syns1)
        if distance > 3:
          sentence = text_NPs[np][0].strip() + '.'
          if sentence in sentences:
            sentences[sentence] = sentences[sentence].replace(np, '**%s**' % np)
          else:
            sentences[sentence] = sentence.replace(np, '**%s**' % np)

    syns1 = []
    for vp in article1_VPs:
      syn = wn.synsets(vp, 'v')
      if syn:
        syn = syn[0]
        syns1.append(syn)
        syns1.extend(get_ancestors(syn))

    for verb in diff_VPs:
      verb = verb.encode('utf-8')
      syn = wn.synsets(verb, 'v')
      if syn:
        syn = syn[0]
        distance = synset_distance(syn, syns1)
        if distance > 5 and distance != float("inf"):
          sentence = text_VPs[verb][0].encode('utf-8').strip() + '.'
          if sentence in sentences:
            sentences[sentence] = sentences[sentence].replace(verb, '**%s**' % verb)
          else:
            sentences[sentence] = sentence.replace(verb, '**%s**' % verb)

    return sentences.values()

def differential(article, comparison_articles):
  '''Compares article to the comparison_articles.

  Args:
    article: an Article
    comparison_articles: a list of Articles to be compared to Article

  Returns:
    The list of comparison_articles in JSON format, with a 'sentences'
    attribute containing a list of sentences with different facts from the
    original article.
    '''
  all_results = []
  for comparison_article in comparison_articles:
    comparison_results = comparison_article.to_dict()
    comparison_results['sentences'] = compare_articles(article,
                                                       comparison_article)
    all_results.append(comparison_results)
  return json.dumps(all_results)

if __name__ == '__main__':
  '''
  with open('test_articles/article1.json') as article1:
    article1 = json.load(article1)

    with open('test_articles/article2.json') as article2:
      article2 = json.load(article2)

      print [val for val in compare_articles(article1, article2)]
      '''
