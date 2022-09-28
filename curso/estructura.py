import spacy

nlp = spacy.load("es_core_news_sm")
doc = nlp("Yo tengo un gato")

# Busca el hash para la palabra "gato"
gato_hash = nlp.vocab.strings["gato"]
print(gato_hash)

# Busca el gato_hash para obtener el string
gato_string = nlp.vocab.strings[gato_hash]
print(gato_string)

doc = nlp("David Bowie tiene el label PER")

# Busca el hash para el label del string "PER"
person_hash =  nlp.vocab.strings["PER"]
print(person_hash)

# Busca el person_hash para obtener el string
person_string = nlp.vocab.strings[person_hash]
print(person_string)

# Crea un objeto nlp de español y uno de alemán
nlp = spacy.blank("es")
nlp_de = spacy.blank("de")

doc = nlp_de("David Bowie tiene el label PER")

# Obtén el ID para el string "Bowie"
bowie_id = nlp_de.vocab.strings["Bowie"]
print(bowie_id)

# Busca el ID de "Bowie" en el vocabulario
print(nlp_de.vocab.strings[bowie_id])

# Importa las clases Doc y Span
from spacy.tokens import Doc, Span

# Las palabras y espacios que usaremos para crear el doc
words = ["¡", "Hola", "Mundo", "!"]
spaces = [False, True, False, False]

# Crea un doc manualmente
doc = Doc(nlp.vocab, words=words, spaces=spaces)

# Crea un span manualmente
span = Span(doc, 1, 3)

# Crea un span con un label
span_with_label = Span(doc, 1, 3, label="SALUDO")

# Añade el span a los doc.ents
doc.ents = [span_with_label]

#import spacy
#nlp = spacy.load("es_core_news_sm")
# Importa la clase Doc
#from spacy.tokens import Doc, Span

# El texto deseado: "spaCy es divertido!"
words = ["spaCy", "es", "divertido", "!"]
spaces = [True, True, False, False]

# Crea un Doc a partir de las palabras y los espacios
doc2 = Doc(nlp.vocab, words=words, spaces=spaces)
print(doc2.text)

# El texto deseado: "¡Vamos, empieza!"
words = ["¡", "Vamos", ",", "empieza", "!"]
spaces = [False, False, True, False, False]

# Crea un Doc a partir de las palabras y los espacios
doc3 = Doc(nlp.vocab, words=words, spaces=spaces)
print(doc3.text)

# El texto deseado: "¡¿En serio?!"
words = ["¡", "¿", "En", "serio", "?", "!"]
spaces = [False, False, True, False, False, False]

# Crea un Doc a partir de las palabras y los espacios
doc4 = Doc(nlp.vocab, words=words, spaces=spaces)
print(doc4.text)

words = ["Me", "gusta", "David", "Bowie"]
spaces = [True, True, True, False]

# Crea un doc a partir de las palabras y los espacios
doc5 = Doc(nlp.vocab, words=words, spaces=spaces)
print(doc5.text)

# Crea un span para "David Bowie" a partir del doc y asígnalo al label "PERSON"
span2 = Span(doc5, 2,3,label="PER")
print(span.text, span.label_)

# Añade el span a las entidades del doc
doc5.ents = [span2]

# Imprime en pantalla el texto y los labels de las entidades
print([(ent.text, ent.label_) for ent in doc5.ents])

nlp = spacy.load("es_core_news_sm")

doc = nlp("Por Berlín fluye el río Esprea.")

# Itera sobre los tokens
for token in doc:
    #print(token.pos_)
    # Revisa si el token actual es un nombre propio
    if token.pos_ == "PROPN":
        # Revisa si el siguiente token es un verbo
        if doc[token.i + 1].pos_ == "VERB":
            print("Encontré un nombre propio antes de un verbo:", token.text)