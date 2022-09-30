import re
import spacy
from spacy.language import Language
from spacy.tokens import Token
from instagrapi import Client
import time
import re
import geonamescache

gc = geonamescache.GeonamesCache()

#cl = Client()
#cl.login(" betitoprendido3", "challenge/action/1")

#nlp = spacy.load("en_core_web_trf")
nlp = spacy.blank("es")

@Language.component("mention_hashtags")
def mention_hashtags(doc):
    i = []
    for token_index, token in enumerate(doc):
            if token.text== "#" or token.text=="@":
                i.append(token_index)

    for idx, token_pos in enumerate(i):
        with doc.retokenize() as retokenizer:
            token_pos = token_pos - idx
            retokenizer.merge(doc[token_pos: token_pos+2])
    return doc

@Language.component("mention_hashtags_set_extension")
def mention_hashtags_set_extension(doc):
    hashtag_getter = lambda token: token.text.startswith('#')
    Token.set_extension('is_hashtag', getter=hashtag_getter)
    mention_getter = lambda token: token.text.startswith('@')
    Token.set_extension('is_mention', getter=mention_getter)
    return doc

@Language.component("local_set_extension")
def loc_set_extension(doc):
    wordlist = initialize_words("wl")
    Token.set_extension("is_geo", default=False)
    Token.set_extension("geo_countrycode", default=None)
    print(type(wordlist))
    for token_index, token in enumerate(doc):
        if token._.is_hashtag:
            #print("token es hashtag en componente",token.text)
            parse_tag(token, token.text, wordlist)
            #if token.text in wordlist:
            #    print("lo encontró")
            #    print(token)
    return doc

#none
# Returns a list of common english terms (words)
def initialize_words(dict_txt):
    content = None
    with open(dict_txt+'.txt', encoding='UTF-8') as f: # A file containing common english words
        content = f.readlines()
        print("Initialize Words", dict_txt, "file")
    return [word.rstrip('\n') for word in content]

def parse_sentence(sentence, wordlist):
    #print("parse_sentence")
    new_sentence = "" # output
    terms = sentence.split(' ')
    #print(terms)
    for term in terms:
        #print(term)
        if not term == "":
            if term[0] == '#': # this is a hashtag, parse it
                new_sentence += parse_tag(term, wordlist)
            else: # Just append the word
                new_sentence += term
            new_sentence += " "

    return new_sentence

def parse_tag(token, term, wordlist):
    #print("parse_tag", term)
    words = []
    # Remove hashtag, split by dash
    tags = term[1:].split(' ')
    print("Tags despues de split", tags)
    for tag in tags:
        print("Tags despues de split for each", tag)
        word = find_word(token, tag, wordlist)
        print("despues find_word")
        while word != None and len(tag):
            words.append(word)
            print("algo pasa?")
            if len(tag) == len(word): # Special case for when eating rest of word
                break
            tag = tag[len(word):]
            word = find_word(token, tag, wordlist)
    return(" ".join(words))

def find_word(token, tag, wordlist):
    print("find_word():", tag)
    i = len(tag) + 1
    while i > 1:
        i -= 1
        if tag[:i] in wordlist and len(tag[:i]):
            print("find_word() inlist:",tag[:i])
            city = gc.search_cities(tag[:i], case_sensitive=False)
            e = 0
            while e < len(city):
                if (city[e]['countrycode'] == "CA") or (city[e]['countrycode'] == "MX") or (city[e]['countrycode'] == "US"):
                    token._.is_geo = True
                    token._.set("geo_countrycode",city[e]['countrycode'])
                    print(tag[:i], "is geo")
                    print(city[e])
                e += 1
            return tag[:i]
    return None



nlp.add_pipe("mention_hashtags", first=True)
nlp.add_pipe("mention_hashtags_set_extension", after="mention_hashtags")
nlp.add_pipe("local_set_extension", after="mention_hashtags_set_extension")

s = """#winnipegbench #canadabench #jaliscograffiti #benchguadalajara #bombasguadalajaramistrik #jasdjaws #jawscaminojalisco #tlajomulco #guadalajaragraffiti"""
s = re.sub(r'#', r' #', s)
doc = nlp(s)

for token in doc:
    if not token.is_space:
        print(token.text, token.lemma_, token.pos_)
        if token._.is_geo:
            #time.sleep(5)
            #print(token.text, " - ", cl.user_info_by_username(token_mention).biography)
            print(token.text, " - geo -", token._.geo_countrycode)