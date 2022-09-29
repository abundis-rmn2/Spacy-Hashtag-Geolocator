import spacy
from spacy.matcher import Matcher
from spacy.matcher import PhraseMatcher
from spacy.tokens import Span

import geonamescache
import re

gc = geonamescache.GeonamesCache()
def gen_dict_extract(var, key):
    if isinstance(var, dict):
        for k, v in var.items():
            if k == key:
                yield v
            if isinstance(v, (dict, list)):
                yield from gen_dict_extract(v, key)
    elif isinstance(var, list):
        for d in var:
            yield from gen_dict_extract(d, key)

# gets nested dictionary for countries
countries = gc.get_countries()
# gets nested dictionary for cities
cities = gc.get_cities()

cities = [*gen_dict_extract(cities, 'name')]
countries = [*gen_dict_extract(countries, 'name')]

nlp = spacy.blank("en")
matcher = PhraseMatcher(nlp.vocab, attr="LOWER")

# Only run nlp.make_doc to speed things up
patterns = [nlp.make_doc(text) for text in cities]
pattern = [{'TEXT': {'REGEX': '\d{1}[a|p]m'}}]
matcher.add("TerminologyList", patterns)

s = """#pegados#etiquetas#otraetiqueta @rrrmn2 #hashtags #🦫 REPUS 🦫
Have a good day, humans! #guadalajarabench guadalajara jalisco tlajomulco obama winnipeg guadalajara 

#repus #repusgraffiti #repusbeaver #hoppergraffiti #fr8painting #fr8traingraffiti #fr8porn #benching #benchingtrains #trainbenching #winnipegbench #canadabench"""
s = re.sub(r'#', r' #', s)
doc = nlp(s)
matches = matcher(doc)

for match_id, start, end in matches:
    span = doc[start:end]
    print(span)
