from nltk.tokenize import sent_tokenize
import nltk

#nltk.download('punkt')
text = '''
es definitivamente asqueroso, y al parecer no para de absorber todo lo que nos importa, llegará un punto en el que el progresismo se volverá la nueva normativa.
'''
def split_into_sentences(text: str) -> list[str]:
    text = text.strip()
    text = text.replace(",",".<stop>")
    text = text.replace(".",".<stop>")
    text = text.replace("?","?<stop>")
    text = text.replace("!","!<stop>")
    sentences = text.split("<stop>")
    sentences = [s.strip() for s in sentences]
    sentences = list(filter(None, sentences))
    #if sentences and not sentences[-1]: sentences = sentences[:-1]
    return sentences


blob = split_into_sentences(text)
i = 0
for sentence in blob:
    i = i +1
    print(str(i) + ")" + sentence)
