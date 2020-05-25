import spacy
nlp = spacy.load("es_core_news_md")

document = nlp("Gracias")
adv = []
time = []
for i, s in enumerate(document.sents):
    for j, token in enumerate(s):
        if token.tag_ == 'ADV___':
            adv.append(token.orth_)
        if token.tag_ == 'NOUN__AdvType=Tim' or token.tag_ == "NUM__NumForm=Digit|NumType=Card":
            time.append(token.orth_)
        print("palabra", token.orth_,token.pos_,token.tag_,token.lemma_,token.shape_)
print(adv)
print(time)



# document = nlp("¿Cuál es el nivel de aire hoy?")
# for i, s in enumerate(document.sents):
#     for j, token in enumerate(s):
#         print("palabra", token.orth_,token.pos_,token.tag_,token.lemma_,token.shape_)

# document = nlp("¿Cuál será el nivel de aire mañana?")
# for i, s in enumerate(document.sents):
#     for j, token in enumerate(s):
#         print("palabra", token.orth_,token.pos_,token.tag_,token.lemma_,token.shape_)

# document = nlp("Esta frase no tiene sentido")
# for i, s in enumerate(document.sents):
#     for j, token in enumerate(s):
#         print("palabra", token.orth_,token.pos_,token.tag_,token.lemma_,token.shape_)

# document = nlp("¿Cuál será el nivel del aire el día 20 de mayo a las 12 de la mañana?")
# for i, s in enumerate(document.sents):
#     for j, token in enumerate(s):
#         print("palabra", token.orth_,token.pos_,token.tag_,token.lemma_,token.shape_)