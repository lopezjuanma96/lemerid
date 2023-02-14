import re
import eng_to_ipa as eti
from separasilabas import silabizer

sb = silabizer()

def load(path):
    with open(path, encoding='utf-8') as f:
        text = f.read().lower()

    clean = re.sub(r'(\.|\,|\¡|\!|\¿|\?)', r' \1 ', text) #separate specific punctuation
    clean = re.sub(r'\&', 'and', clean) #replace symbols with words
    clean = re.sub(r'[^ \w\.\,\¡\!\¿\?]', r' ', clean) #strip other symbols (replace with space and later multiple spaces are deleted)
    clean = re.sub(r' {2,}', r' ', clean)

    return clean


def process(text, language):
    proc = []
    vocabulary = {'<BEG>', '<SPA>', '<END>', '<NULL>'} #beggining, end, space, and null (for vocabulary elements that don't appear on the training set)

    proc.append('<BEG>')
    for word in text.split(' '):
        if word == '' or word.isspace(): #even doing regex sub some words spaces or emprty strings may end up appearing.
            continue

        if word in ['.', ',', '¡', '!', '¿', '?']:
            punct = f'<{word}>'
            vocabulary.add(punct)
            proc.append(punct)
            continue
        
        if language == 'en':
            phonems = [ph[0] for ph in eti.ipa_list(word)] #ph[0] bc eti return a list with list of phonems in case some phonem has different forms of being presented.
        elif language == 'es':
            phonems = sb(word)
        else:
            raise ValueError(f'Language provided on PARAMS, {language}, has no support.')
        
        for ph in phonems:
            vocabulary.add(ph) #since it's a set, i don't have to care about checking it ph is already on it
            proc.append(ph)
        proc.append('<SPA>')
    proc.append('<END>')

    return proc, vocabulary