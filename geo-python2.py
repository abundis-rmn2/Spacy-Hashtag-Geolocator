import re
import geonamescache

gc = geonamescache.GeonamesCache()

# hashtag_split from https://stackoverflow.com/questions/20516100/term-split-by-hashtag-of-multiple-words

# Returns a list of common english terms (words)
def initialize_words():
    content = None
    with open('wl.txt', encoding='UTF-8') as f: # A file containing common english words
        content = f.readlines()
    return [word.rstrip('\n') for word in content]

def parse_sentence(sentence, wordlist):
    print("parse_sentence", sentence)
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

def parse_tag(term, wordlist):
    print("parse_tag", term)
    words = []
    # Remove hashtag, split by dash
    tags = term[1:].split('-')
    for tag in tags:
        word = find_word(tag, wordlist)
        while word != None and len(tag) > 0:
            words.append(word)
            if len(tag) == len(word): # Special case for when eating rest of word
                break
            tag = tag[len(word):]
            word = find_word(tag, wordlist)
    return " ".join(words)

def find_word(token, wordlist):
    print("find_word", token)
    i = len(token) + 1
    while i > 1:
        i -= 1
        if token[:i] in wordlist and len(token[:i]):
            print("inlist", token[:i])
            return token[:i]
    return None


wordlist = initialize_words()
s = """#winnipegbench #canadabench #jaliscograffiti #benchguadalajara #graffitiguadalajara"""
s = re.sub(r'#', r' #', s)
#print(parse_sentence(sentence, wordlist))

list = parse_sentence(s, wordlist).split(" ")
for token in list:
    if not token == "":
        print(token)
        city = gc.search_cities(token, case_sensitive=False)
        i = 0
        while i < len(city):
            if (city[i]['countrycode'] == "CA") or (city[i]['countrycode'] == "MX") or (city[i]['countrycode'] == "US"):
                print(city[i])
            i += 1