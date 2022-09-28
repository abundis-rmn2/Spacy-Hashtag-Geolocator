import spacy

nlp = spacy.load("es_core_news_lg")

# Imprime en pantalla los nombres de los componentes del pipeline
print(nlp.pipe_names)

# Imprime en pantalla el pipeline entero de tuples (name, component)
print(nlp.pipeline)