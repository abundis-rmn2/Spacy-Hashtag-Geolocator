import spacy
from spacy.tokens import Token
from spacy.tokens import Doc
from spacy.tokens import Span

nlp = spacy.blank('es')

# Registra la extensión de atributo del Token, "is_country",
# con el valor por defecto False
#____.____(____, ____=____)
Token.set_extension("is_country", default=False)

# Procesa el texto y pon True para el atributo "is_country"
# para el token "España"
doc = nlp("Vivo en España.")
doc[2]._.is_country = True

# Imprime en pantalla el texto del token y el atributo "is_country"
# para todos los tokens
print([(token.text, token._.is_country) for token in doc])

# Define la función getter que toma un token y devuelve su texto al revés
def get_reversed(token):
    return token.text[::-1]


# Registra la extensión de propiedad del Token, "reversed", con
# el getter get_reversed
#____.____(____, ____=____)
Token.set_extension("reversed", getter=get_reversed)

# Procesa el texto e imprime en pantalla el atributo "reversed"
# para cada token
doc = nlp("Todas las generalizaciones son falsas, incluyendo esta.")
for token in doc:
    print("Normal:", token.text)
    print("invertido:", token._.reversed)

# Define la función getter
def get_has_number(doc):
    # Devuelve si alguno de los tokens en el doc devuelve True
    # para token.like_num
    return any(token.like_num for token in doc)


# Registra la extensión de propiedad del Doc, "has_number",
# con el getter get_has_number
#____.____(____, ____=____)
Doc.set_extension("has_number", getter=get_has_number)

# Procesa el texto y revisa el atributo personalizado "has_number"
doc = nlp("El museo cerró por cinco años en el 2012.")
print("has_number:", doc._.has_number)
for token in doc:
    print("Normal:", token.text)
    print("invertido:", token._.reversed)

# Define el método
def to_html(span, tag):
    # Envuelve el texto del span en un HTML tag y devuélvelo
    return f"<{tag}>{span.text}</{tag}>"


# Registra la extensión de propiedad del Span, "to_html",
# con el método "to_html"
#____.____(____, ____=____)
Span.set_extension("to_html", method=to_html)

# Procesa el texto y llama el método "to_html"en el span
# con el nombre de tag "strong"
doc = nlp("Hola mundo, esto es una frase.")
span = doc[0:2]
print(span._.to_html("strong"))