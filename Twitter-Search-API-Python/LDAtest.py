from nltk.tokenize import RegexpTokenizer
from stop_words import get_stop_words
from nltk.stem.porter import PorterStemmer
from gensim import corpora, models
import gensim
import json
tokenizer = RegexpTokenizer(r'\w+')

# create English stop words list
en_stop = get_stop_words('en')

# Create p_stemmer of class PorterStemmer
p_stemmer = PorterStemmer()

# create sample documents
doc_a = "Brocolli is good to eat. My brother likes to eat good brocolli, but not my mother."
doc_b = "My mother spends a lot of time driving my brother around to baseball practice."
doc_c = "Some health experts suggest that driving may cause increased tension and blood pressure."
doc_d = "I often feel pressure to perform well at school, but my mother never seems to drive my brother to do better."
doc_e = "Health professionals say that brocolli is good for your health."
# compile sample documents into a list

doc_set = [doc_a, doc_b, doc_c, doc_d, doc_e]
doc_set.clear()
with open ('/Users/licheng5625/PythonCode/masterarbeit/data/webpagefortwitter/Tweet_JSON/rumors/appreciation_month_muslim.txt',mode='r') as doc:
    for line in doc:
        JSON=json.loads(line)
        for url in JSON['urls']:
            JSON['text']=JSON['text'].replace(url,'')
        doc_set.append(JSON['text'])
print(len(doc_set))

# list for tokenized documents in loop
texts = []

# loop through document list
for i in doc_set:

    # clean and tokenize document string
    raw = i.lower()
    tokens = tokenizer.tokenize(raw)
    mystop=['www','http','com']
    # remove stop words from tokens
    stopped_tokens=[]
    for i in tokens:
        if i not in en_stop and i not in mystop and len(i)>1:
            stopped_tokens.append(i)
    #stopped_tokens = [i for i in tokens if not i in en_stop]

    # stem tokens
    stemmed_tokens = [p_stemmer.stem(i) for i in stopped_tokens]

    # add tokens to list
    texts.append(stemmed_tokens)

# turn our tokenized documents into a id <-> term dictionary
dictionary = corpora.Dictionary(texts)

# convert tokenized documents into a document-term matrix
corpus = [dictionary.doc2bow(text) for text in texts]

# generate LDA model
ldamodel = gensim.models.ldamodel.LdaModel(corpus, num_topics=5, id2word = dictionary, passes=20)
print(ldamodel.print_topics(num_topics=5 ))
#topic inference
#boilerplate

#boilerpipe