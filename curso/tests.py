import spacy

# Crea un objeto nlp vacío para procesar español
nlp = spacy.blank("es")

doc = nlp("¡Hola Mundo!")

# Itera sobre los tokens en un Doc
for token in doc:
    print(token.text)

doc = nlp("Eso cuesta €5.")
print("Índice:   ", [token.i for token in doc])
print("Texto:    ", [token.text for token in doc])

print("is_alpha:", [token.is_alpha for token in doc])
print("is_punct:", [token.is_punct for token in doc])
print("like_num:", [token.like_num for token in doc])


# Procesa el texto
doc = nlp("Me gustan las panteras negras y los leones.")

# Un slice del Doc para "panteras negras"
panteras_negras = doc[3:5]
print(panteras_negras.text)

# Un slice del Doc para "panteras negras y los leones" (sin el ".")
panteras_negras_y_leones = doc[3:8]
print(panteras_negras_y_leones.text)

# Procesa el texto
doc = nlp(
    "En 1990, más del 60 % de las personas en Asia del Este se encontraban "
    "en extrema pobreza. Ahora, menos del 4 % lo están."
)

# Itera sobre los tokens en el doc
for token in doc:
    # Revisa si el token parece un número
    if token.like_num:
        # Obtén el próximo token en el documento
        next_token = doc[token.i + 1]
        # Revisa si el texto del siguiente token es igual a '%'
        if next_token.text == "%":
            print("Porcentaje encontrado:", token.text)