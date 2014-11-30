import nltk
import json

with open('output_json_files/jpost_output.json') as data_file: 
    data = json.load(data_file)

query = data["title"]



text_pre = query #"""What really happened with NBC and Ayman Mohyeldin"""
text_pre = text_pre.lower()
from nltk.corpus import stopwords
stopwords = stopwords.words('english')
text = ""
for word in text_pre.split(" "):
    if word not in stopwords:
        text += word + " "

#print text

#The Buddha, the Godhead, resides quite as comfortably in the circuits of a digital
#computer or the gears of a cycle transmission as he does at the top of a mountain
#or in the petals of a flower. To think otherwise is to demean the Buddha...which is
#to demean oneself."""
 
# Used when tokenizing words
sentence_re = r'''(?x)      # set flag to allow verbose regexps
      ([A-Z])(\.[A-Z])+\.?  # abbreviations, e.g. U.S.A.
    | \w+(-\w+)*            # words with optional internal hyphens
    | \$?\d+(\.\d+)?%?      # currency and percentages, e.g. $12.40, 82%
    | \.\.\.                # ellipsis
    | [][.,;"'?():-_`]      # these are separate tokens
'''
 
lemmatizer = nltk.WordNetLemmatizer()
stemmer = nltk.stem.porter.PorterStemmer()
 
#Taken from Su Nam Kim Paper...
grammar = r"""
    NBAR:
        {<NN.*|JJ>*<NN.*>}  # Nouns and Adjectives, terminated with Nouns
        
    NP:
        {<NBAR>}
        {<NBAR><IN><NBAR>}  # Above, connected with in/of/etc...
"""
chunker = nltk.RegexpParser(grammar)

        
toks = nltk.regexp_tokenize(text, sentence_re)
postoks = nltk.tag.pos_tag(toks)


query = ""

for (word,tag) in postoks:
    if tag == "NN":
        query += word + " "


print query
