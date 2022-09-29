import re
import spacy
from spacy.language import Language
from spacy.tokens import Token
from instagrapi import Client
import time

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


nlp.add_pipe("mention_hashtags", first=True)
nlp.add_pipe("mention_hashtags_set_extension", after="mention_hashtags")

s = """#pegados#etiquetas#otraetiqueta @rrrmn2 #hashtags #🦫 REPUS 🦫
Have a good day, humans!

#repus #repusgraffiti #repusbeaver #hoppergraffiti #fr8painting #fr8traingraffiti #fr8porn #benching #benchingtrains #trainbenching #winnipegbench #canadabench"""
s = re.sub(r'#', r' #', s)
doc = nlp(s)

for token in doc:
    if not token.is_space:
        if token._.is_hashtag:
            #time.sleep(5)
            token_hashtag = re.sub(r'#', r'', token.text)
            #print(token.text, " - ", cl.hashtag_info(token_hashtag).media_count)
            print(token.text, " - hashtag")
        elif token._.is_mention:
            #time.sleep(5)
            token_mention = re.sub(r'@', r'', token.text)
            #print(token.text, " - ", cl.user_info_by_username(token_mention).biography)
            print(token.text, " - arroba ")