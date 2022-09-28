import spacy
# Carga uno de los modelos más grandes que contiene vectores
nlp_en = spacy.load('en_core_web_lg')
nlp_es = spacy.load("es_core_news_lg")
nlp = spacy.blank("es")

# Inicializa con el vocabulario compartido
from spacy.matcher import Matcher
matcher = Matcher(nlp_es.vocab)

# Los patrones son listas de diccionarios que describen los tokens
pattern = [{"LEMMA": "comer", "POS": "VERB"}, {"LOWER": "pizza"}]
matcher.add("PIZZA", [pattern])

# Los operadores pueden especificar qué tan seguido puede
# ser buscado un token
pattern = [{"TEXT": "muy", "OP": "+"}, {"TEXT": "feliz"}]
matcher.add("MUY_FELIZ", [pattern])

# Llamar al matcher sobre un doc devuelve una lista de
# tuples con (match_id, inicio, final)
doc = nlp_es("Me gusta comer pizza y estoy muy muy feliz")
matches = matcher(doc)

print(matches)

matcher.add("PERRO", [[{"LOWER": "labrador"}, {"LOWER": "dorado"}]])
doc = nlp_es("Tengo un labrador dorado")

for match_id, start, end in matcher(doc):
    print(match_id)
    print(start)
    print(end)
    span = doc[start:end]
    print("span encontrado:", span.text)
    # Obtén el token raíz del span y el token raíz cabeza (head)
    print("Token raíz:", span.root.text)
    print("Token raíz cabeza:", span.root.head.text)
    # Obtén el token anterior y su POS tag
    print("Token anterior:", doc[start - 1].text, doc[start - 1].pos_)

from spacy.matcher import PhraseMatcher

matcher = PhraseMatcher(nlp.vocab)

pattern = nlp_es("labrador dorado")
matcher.add("PERRO", [pattern])
doc = nlp_es("Tengo un labrador dorado")

# Itera sobre los resultados
for match_id, start, end in matcher(doc):
    print(match_id)
    print(start)
    print(end)
    span = doc[start:end]
    print("span encontrado:", span.text)
    # Obtén el token raíz del span y el token raíz cabeza (head)
    print("Token raíz:", span.root.text)
    print("Token raíz cabeza:", span.root.head.text)
    # Obtén el token anterior y su POS tag
    print("Token anterior:", doc[start - 1].text, doc[start - 1].pos_)