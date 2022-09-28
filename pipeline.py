import spacy

nlp = spacy.load("es_core_news_sm")

text = (
    "Los Olímpicos de Tokio 2020 son la inspiración para la nueva "
    "colección de zapatillas adidas zx."
)

# Procesa un texto
doc = nlp(text)

# Itera sobre los tokens
for token in doc:
    print("______________________")
    # Imprime en pantalla el texto y la etiqueta gramatical predicha
    #print(token.text, token.pos_)
    token_text = token.text
    token_pos = token.pos_
    token_dep = token.dep_
    print("Etiqueta gramatical")
    print(spacy.explain(token_pos))
    print("Etiqueta de dependencia sintática")
    print(spacy.explain(token_dep))
    # Esto es solo por formato
    print(f"{token_text:<12}{token_pos:<10}{token_dep:<10}")

# Itera sobre las entidades predichas
for ent in doc.ents:
    # Imprime en pantalla el texto de la entidad y su etiqueta
    print(ent.text, ent.label_)

# Obtén el span para "adidas zx"
adidas_zx = doc[14:16]

# Imprime en pantalla el texto del span
print("Entidad faltante:", adidas_zx.text)

# Importa el Matcher
from spacy.matcher import Matcher

# Inicializa el matcher con el vocabulario compartido
matcher = Matcher(nlp.vocab)

# Crea un patrón que encuentre dos tokens: "adidas" y "zx"
pattern = [{"TEXT": "adidas"}, {"TEXT": "zx"}]

# Añade el patrón al matcher
matcher.add("ADIDAS_ZX_PATTERN", [pattern])

# Usa al matcher sobre el doc
matches = matcher(doc)
print("Resultados:", [doc[start:end].text for match_id, start, end in matches])

doc = nlp(
    "Después de hacer la actualización de iOS no notarás un rediseño "
    "radical del sistema: no se compara con los cambios estéticos que "
    "tuvimos con el iOS 7. La mayoría de las funcionalidades del iOS 11 "
    "siguen iguales en el iOS 10."
)

# Escribe un patrón para las versiones de iOS completas
# ("iOS 7", "iOS 11", "iOS 10")
pattern = [{"TEXT": "iOS"}, {"IS_DIGIT": True}]

# Añade el patrón al matcher y usa el matcher sobre el documento
matcher.add("IOS_VERSION_PATTERN", [pattern])
matches = matcher(doc)
print("Total matches found:", len(matches))

# Itera sobre los resultados e imprime el texto del span
for match_id, start, end in matches:
    print("Match found:", doc[start:end].text)

doc = nlp(
    "descargué Fortnite en mi computadora, pero no puedo abrir el juego. "
    "Ayuda? Cuando estaba descargando Minecraft, conseguí la versión de Windows "
    "donde tiene una carpeta '.zip' y usé el programa por defecto para "
    "descomprimirlo…así que también tengo que descargar Winzip?"
)

# Escribe un patrón que encuentre una forma de "descargar" más un nombre propio
pattern = [{"LEMMA": "descargar"}, {"POS": "PROPN"}]

# Añade el patrón al matcher y usa el matcher sobre el documento
matcher.add("DOWNLOAD_THINGS_PATTERN", [pattern])
matches = matcher(doc)
print("Total de resultados encontrados:", len(matches))

# Itera sobre los resultados e imprime el texto del span
for match_id, start, end in matches:
    print("Resultado encontrado:", doc[start:end].text)

doc = nlp(
    "El gigante tecnológico IBM está ofreciendo lecciones virtuales "
    "sobre tecnologías avanzadas gratuitas en español."
)

# Escribe un patrón para un sustantivo más uno o dos adjetivos
pattern = [{"POS": "NOUN"}, {"POS": "ADJ"}, {"POS": "ADJ", "OP": "?"}]

# Añade el patrón al matcher y usa el matcher sobre el documento
matcher.add("NOUN_ADJ_PATTERN", [pattern])
matches = matcher(doc)
print("Total de resultados encontrados:", len(matches))

# Itera sobre los resultados e imprime el texto del span
for match_id, start, end in matches:
    print("Resultado encontrado:", doc[start:end].text)