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
    wordlistarr = initialize_words("wl").splitlines()
    #print(wordlist)
    Token.set_extension("is_geo", default=False)
    Token.set_extension("geo_countrycode", default=None)
    print(type(wordlist))
    for token_index, token in enumerate(doc):
        if token._.is_hashtag:
            #print("token es hashtag en componente",token.text)
            parse_tag(token, token.text, wordlist, wordlistarr)
            #if token.text in wordlist:
            #    print("lo encontró")
            #    print(token)
    return doc

# Returns a list of common english terms (words)
def initialize_words(dict_txt):
    content = None
    content_clean = ""
    with open(dict_txt+'.txt', encoding='UTF-8') as f: # A file containing common english words
        content = f.readlines()
        print("Initialize Words", dict_txt, "file")
    #return [word.lower().rstrip('\n') for word in content]
    print(type(content))
    print(len(content))
    for word in content:
        #print(word)
        if ' ' in word:
            content_clean += word.lower().rstrip('\n')
            content_clean += "\n"
            word = word.replace(" ", "")
            #print("after replace", word)
            content_clean += word.lower()
        else:
            content_clean += word.lower().rstrip('\n')+" "
            content_clean += "\n"
    return content_clean.rstrip('\n')

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

def parse_tag(token, term, wordlist, wordlistarr):
    #print("parse_tag", term)
    words = []
    # Remove hashtag, split by dash
    tags = term[1:].split(' ')
    #print("Tags despues de split", tags)
    for tag in tags:
        #print("Tags despues de split for each", tag)
        word = find_word(token, tag, wordlist, wordlistarr)
        #print("despues find_word")
        while word != None and len(tag):
            words.append(word)
            #print("algo pasa?")
            if len(tag) == len(word): # Special case for when eating rest of word
                break
            tag = tag[len(word):]
            word = find_word(token, tag, wordlist, wordlistarr)
    return(" ".join(words))

def find_word(token, tag, wordlist, wordlistarr):
    print("find_word() looking for:", tag)
    tag = tag.lower()
    i = len(tag) + 1
    while i > 1:
        i -= 1
        if tag[:i] in wordlist and len(tag[:i]):
            print("find_word() inlist:",tag[:i])
            city = gc.search_cities(tag[:i], case_sensitive=False)
            if not len(city) == 0:
                city_arr(city, i, tag, token)
            elif tag[:i] in wordlistarr:
                #print("encontro algo: tag", tag[:i])
                #print("en el arreglo: ",wordlistarr[wordlistarr.index(tag[:i])])
                #print("en el arreglo: ",wordlistarr[wordlistarr.index(tag[:i])-1])
                city = gc.search_cities(wordlistarr[wordlistarr.index(tag[:i])-1], case_sensitive=False)
                #print(city)
                if not len(city) == 0:
                    city_arr(city, i, tag, token)
            return tag[:i]
    return None

def city_arr(city, i, tag, token):
    print("tag en lista de ciudades")
    e = 0
    #Sort cities by population, biggest cities will get on top
    city = sorted(city, key=lambda e: e['population'], reverse=False)
    while e < len(city):
        if (city[e]['countrycode'] == "CA") or (city[e]['countrycode'] == "MX") or (city[e]['countrycode'] == "US"):
            print(i, tag[:i], "is geo")
            token._.is_geo = True
            token._.set("geo_countrycode", city[e]['countrycode'])
            print(city[e])
        e += 1

nlp.add_pipe("mention_hashtags", first=True)
nlp.add_pipe("mention_hashtags_set_extension", after="mention_hashtags")
nlp.add_pipe("local_set_extension", after="mention_hashtags_set_extension")

s = """#cherokeetag #NorthPekin #SanFrancisco #SanSebastianelGrande #ScottAirForceOne #BuenaVista #WestlakeVillage #winnipegbench #graffiticholula #graffititoluca #canadabench #jaliscograffiti #benchguadalajara #bombasguadalajaramistrik #jasdjaws #jawscaminojalisco #tlajomulco #guadalajaragraffiti"""
s = re.sub(r'#', r' #', s)
doc = nlp(s)

for token in doc:
    if not token.is_space:
        print(token.text, token.lemma_, token.pos_)
        if token._.is_hashtag:
            #time.sleep(5)
            token_hashtag = re.sub(r'#', r'', token.text)
            #print(token.text, " - ", cl.hashtag_info(token_hashtag).media_count)
            print(token.text, " - hashtag")
            if token._.is_geo:
                # time.sleep(5)
                # print(token.text, " - ", cl.user_info_by_username(token_mention).biography)
                print(token.text, " - geo -", token._.geo_countrycode)
        elif token._.is_mention:
            #time.sleep(5)
            token_mention = re.sub(r'@', r'', token.text)
            #print(token.text, " - ", cl.user_info_by_username(token_mention).biography)
            print(token.text, " - arroba ")
