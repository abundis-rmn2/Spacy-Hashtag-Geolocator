import spacy

nlp = spacy.load("es_core_news_sm")

text = (
    "Chick-fil-A es una cadena de restaurantes de comida rápida "
    "americana con sede en la ciudad de College Park, Georgia, "
    "especializada en sándwiches de pollo."
)

with nlp.select_pipes(disable="parser"):
    doc = nlp.make_doc(text)
    print (doc)