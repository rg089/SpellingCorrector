import re
from nltk import sent_tokenize, word_tokenize


def sentence_tokenizer(text, use_nltk=False):
    if use_nltk:
        return sent_tokenize(text)
    else:
        sentences = []
        prev = 0
        for i in range(len(text)):
            if text[i] in ".?!,":
                if i!=prev:
                    sentences.append(text[prev:i].strip()+text[i])
                prev = i+1
            elif i==len(text)-1:
                sentences.append(text[prev:i+1].strip())
        return sentences

# print(sentence_tokenizer("This is certainly not fair!!! Mumbai Indians were cruisign along.jd ashjcsa jasvd.   dwjhf asdchj ajcds  . djvs"))

def word_tokenizer(sentence, use_nltk=False):
    pass