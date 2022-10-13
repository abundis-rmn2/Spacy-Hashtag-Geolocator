import re
import spacy
from spacy.language import Language
from spacy.tokens import Token
from instagrapi import Client
import time
import geonamescache
import difflib

#Starting Geonamescache, Instagrapi & Spacy
gc = geonamescache.GeonamesCache()
cl = Client()
#nlp = spacy.load("en_core_web_trf", disable=["tok2vec", "tagger", "parser", "attribute_ruler", "lemmatizer"])
nlp = spacy.load("en_core_web_trf")
#nlp = spacy.blank("es")

# Setting Spacy set extension once.
Token.set_extension("is_city", default=None)
Token.set_extension("is_graffiti_lingo", default=None)
Token.set_extension("is_railroad_lingo", default=None)
# Metadata
Token.set_extension("geo_countrycode", default=None)
Token.set_extension("geo_hashtag", default=None)
Token.set_extension("graffiti_hashtag", default=None)
Token.set_extension("railroad_hashtag", default=None)

# Function to init wordlists
def initialize_words(dict_txt, space_strip = False):
    content = ""
    content_clean = ""
    with open(dict_txt+'.txt', encoding='UTF-8') as f: # A file containing common english words
        content = f.readlines()
        print("Initialize Words", dict_txt, "file")
    #return [word.lower().rstrip('\n') for word in content]
    print(type(content))
    print(len(content))
    if space_strip == True:
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
    elif space_strip == False:
        for word in content:
            #print("No space striping", word)
            content_clean += word.lower().rstrip('\n') + " "
            content_clean += "\n"

    return content_clean.rstrip('\n')

# Global Wordlist
wordlist = initialize_words("wl")
wordlist_arr = wordlist.splitlines()
# print(wordlist)
text_file = open("wl_compiled.txt", "w", encoding="utf-8")
n = text_file.write(str(wordlist))
text_file.close()

# Particular wordlist in this case citiy names. Will take of space and append to array San Francisco -  sanfrancisco.
# this will help in cases people use #SanFranciscoGraffiti hashtag
citieslist_arr = initialize_words("cities", space_strip=True).splitlines()
# print(citieslist_arr)

# Particular wordlist in this case graffiti and railroad lingo.
# this will help in cases people use #SanFranciscoGraffiti hashtag
graffiti_lingo_arr = initialize_words("graffiti-lingo", space_strip=True).splitlines()
railroad_lingo_arr = initialize_words("railroad-lingo", space_strip=True).splitlines()
# print(citieslist_arr)

@Language.component("mention_hashtags")
def mention_hashtags(doc):
    #if token has # or @ keep it together
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
    #Set extension to token if starts with # or @
    hashtag_getter = lambda token: token.text.startswith('#')
    Token.set_extension('is_hashtag', getter=hashtag_getter, force=True)
    mention_getter = lambda token: token.text.startswith('@')
    Token.set_extension('is_mention', getter=mention_getter, force=True)
    return doc

@Language.component("hashtag_splitter_tagger")
def hashtag_splitter_tagger(doc):
    for token_index, token in enumerate(doc):
        if token._.is_hashtag:
            print("Token is_hashtag",token.text)
            parse_tag(token, token.text)
    return doc

# Code taken from this answer - https://stackoverflow.com/a/20518476/19824551
def parse_tag(token, term):
    print("parse_tag", term)
    words = []
    # Remove hashtag, split by dash
    tags = term[1:].split(' ')
    print("tag without #", tags)
    for tag in tags:
        # This loop will look for a word in wordlist, if find something take this word away from hashtag
        # for example the whole hashtag (token) is #freightgraffitiSanFrancisco, this script will look from the start of the string
        # will find "freight" - > use it in find_word() and strip it away from the whole hashtag
        # then will use the string "graffitiSanFrancisco", and then SanFransisco
        print("Tag after word stripping", tag)
        # Here its looking fot the word in the wordlist
        word = find_word(token, tag)
        print("despues find_word")
        while word != None and len(tag):
            words.append(word)
            print("algo pasa?")
            if len(tag) == len(word): # Special case for when eating rest of word
                break
            tag = tag[len(word):]
            word = find_word(token, tag)
    return(" ".join(words))

def find_word(token, tag):
    # Called from parse_tag()
    print("find_word() looking for:", tag)
    tag = tag.lower()
    i = len(tag) + 1
    while i > 1:
        i -= 1
        #print(tag, tag[:i])
        #if tag[:i] in wordlist and len(tag[:i]) > 3: #will do the work, but may flag false positives, next conditional works better but may be slower
        if re.search(r"\b" + re.escape(tag[:i]) + r"\b", wordlist) and len(tag[:i]) > 0: #https://stackoverflow.com/questions/4154961/find-substring-in-string-but-only-if-whole-words
            print("find_word in wordlist:",tag[:i])
            # If a word in globallist is finded will look for it in the city array [Guadalajara, San Franisco, sanfrancisco] ---- This one have all the cities with spaces already stripped and append
            # or any of the two lingo dicts -> graffiti and railroad
            for city in citieslist_arr:
                if string_similarity(tag[:i], city) > .9 and len(tag[:i]) > 5:
                    print("Similarity", tag[:i], city) # Long list of cities, similarity has to real high almost 1
                #if tag[:i] in city and len(tag[:i]) > 5:
                    #print("Tag is in city name", tag[:i], city) # Long list of cities that includes common lenguage words vgr find_word() looking for: rollingcanvas | find_word in wordlist: rolling tag is in city name: rolling - rolling meadows
                #if tag[:i] == city:
                    #print("Exact match", tag[:i], city) # Couldnt make it work
                    # in any case tag its foundend will look for the similar string using Geosnamecache library
                    city = gc.search_cities(tag[:i], case_sensitive=False)
                    # If response is positive, will call function city_arr that will set_extension is_city to the whole token.
                    if not len(city) == 0:
                        city_arr(city, i, tag[:i], token)
                    elif tag[:i] in citieslist_arr:
                    # If answer is negative will look for the next version of the city from sanfrancisco to San Francisco,
                    # supposed to be the next to each other in array
                        print("Found something:", tag[:i])
                        print("in city_list_arr: ",citieslist_arr[citieslist_arr.index(tag[:i])-1])
                        city = gc.search_cities(citieslist_arr[citieslist_arr.index(tag[:i]) - 1], case_sensitive=False)
                        city_arr(city, i, tag[:i], token)

            for graff_lingo in graffiti_lingo_arr:
                if re.search(r"\b" + re.escape(tag[:i]) + r"\b", graff_lingo):
                    print("in graffiti_lingo_arr:")
                    print("Found inside", tag[:i], graff_lingo) #
                    lingo_arr(tag[:i], token, 'is_graffiti_lingo')

            for railroad_lingo in railroad_lingo_arr:
                #if re.search(r"\b" + re.escape(tag[:i]) + r"\b", graff_lingo):
                if string_similarity(tag[:i], railroad_lingo) > .9 and len(tag[:i]) > 3:
                    print("in railroad_lingo_arr: ")
                    print("Found inside", tag[:i], railroad_lingo)  #
                    lingo_arr(tag[:i], token, 'is_railroad_lingo')
            return tag[:i]
    return None

def city_arr(city, i, tag, token):
    e = 0
    #Sort cities by population, biggest cities will get on top
    city = sorted(city, key=lambda e: e['population'], reverse=False)
    #Take more populated city and set countrycode to token
    if (city[0]['countrycode'] == "CA") or (city[0]['countrycode'] == "MX") or (city[0]['countrycode'] == "US") and tag in city[0]['name'].lower(): #Just for México, Canada and USA
    #if tag in city[0]['name'].lower(): # Any Country
        print(i, tag, "is geo")
        token._.set("is_city", True)
        token._.set("geo_countrycode", city[0]['countrycode'])
        token._.set("geo_hashtag", tag)
        print("Hashtag", token.text, "located at:")
        print( city[0])
        e += 1

def lingo_arr(tag, token, lingo_extension):
    if lingo_extension == 'is_graffiti_lingo':
        print("setting", lingo_extension)
        print(token)
        #token._.is_graffiti_lingo: True
        token._.set("is_graffiti_lingo", True)
        token._.set("graffiti_hashtag", tag)
        print(token._.is_graffiti_lingo)
    elif lingo_extension == 'is_railroad_lingo':
        print("setting", lingo_extension)
        print(token)
        token._.set("is_railroad_lingo", True)
        token._.set("railroad_hashtag", tag)
        print(token._.is_railroad_lingo)

#https://www.w3resource.com/python-exercises/string/python-data-type-string-exercise-92.php
def string_similarity(str1, str2):
    result =  difflib.SequenceMatcher(a=str1.lower(), b=str2.lower(), autojunk=False)
    return result.ratio()

nlp.add_pipe("mention_hashtags", first=True)
nlp.add_pipe("mention_hashtags_set_extension", after="mention_hashtags")
nlp.add_pipe("hashtag_splitter_tagger", after="mention_hashtags_set_extension")