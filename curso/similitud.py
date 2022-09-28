import spacy
# Carga uno de los modelos más grandes que contiene vectores
nlp_en = spacy.load('en_core_web_lg')
nlp_es = spacy.load("es_core_news_lg")

# Compara dos documentos
doc1 = nlp_es("Me gusta la comida rápida")
doc2 = nlp_es("Me gusta la pizza")
print(doc1.similarity(doc2))

doc3= nlp_es("Me gustan la pizza y las hamburguesas")
token1 = doc3[3]
token2 = doc3[6]
print(token1.similarity(token2))

# Compara un documento con un token
doc_2 = nlp_es("El camino es largo como el deseo de besar tu entrepierna")
token3 = nlp_es("sexo")[0]

print(doc_2.similarity(token3))

# Compara un span con un documento
span_1 = nlp_es("Me gustan los perros calientes")[3:5]
doc_3 = nlp_es("McDonalds vende hamburguesas")

print(span_1.similarity(doc_3))

doc_vec = nlp_es("Tengo una manzana")
# Accede al vector a través del atributo token.vector
print(doc_vec[2].vector)

# Procesa un texto
doc_4 = nlp_es("Hoy hice pan de banano")

# Obtén el vector para el token "banano"
banano_vector = doc_4[4].vector
print(banano_vector)

doc_5 = nlp_es("Es un cálido día de verano")
doc_6 = nlp_es("Hay sol afuera")

# Obtén la similitud entre el doc1 y el doc2
similarity = doc_5.similarity(doc_6)
print(similarity)

doc_7 = nlp_es(
    "Estuvimos en un restaurante genial. Luego, fuimos a un bar muy divertido."
)

# Crea los spans para "restaurante genial" y "bar muy divertido"
span1_7 = doc_7[3:5]
span2_7 = doc_7[11:14]

# Obtén la similitud entre los dos spans
similarity_7 = span1_7.similarity(span2_7)
print("------")
print(similarity_7)