import json
import spacy

nlp = spacy.load("es_core_news_sm")

with open("twits.json", encoding="utf8") as f:
    TEXTS = json.loads(f.read())

# Procesa los textos e imprime los verbos en pantalla

for doc in nlp.pipe(TEXTS):
    #imprime un arreglo
    print([token.text for token in doc if token.pos_ == "VERB"])
    #imprime en cadeans de texto individuales
    for token in doc:
        if token.pos_ == "VERB":
            print (token.text)

print ("---------------------------------------")
print ("---------------------------------------")

# Procesa los textos e imprime las entidades en pantalla
docs = list(nlp.pipe(TEXTS))
entities = [doc.ents for doc in docs]

for ent in entities:
    for ent_2 in ent:
        print (ent_2.text, "-", ent_2.label_)

print ("---------------------------------------")
print ("---------------------------------------")

people = ["David Bowie", "Angela Merkel", "Lady Gaga"]

# Crea una lista de patrones para el PhraseMatcher
patterns = [nlp(person) for person in people]
print(patterns)
for x in patterns:
    print (x.doc)
print ("---------------------------------------")

patterns = list(nlp.pipe(people))
print(patterns)
for x in patterns:
    print(x)
