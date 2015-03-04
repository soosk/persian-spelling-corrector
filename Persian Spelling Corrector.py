# Author: Morteza Rohanian

# Based on Peter Norvig's article 'How to write a spelling corrector'

# The program uses a subset of Bijankhan's corpus (The corpus distinct words) freely downloadable at
# http://ece.ut.ac.ir/dbrg/bijankhan/

import re, collections

def normalizer(word):
    word = word.replace('ة' ,'ه')
    word = word.replace('ك' ,'ک')
    word = word.replace('ي', 'ی')
    word = word.replace('ؤ', 'و')
    word = word.replace('إ', 'ا')
    return word

def punctuationRemover (word):
    word = re.sub(r'[^\w\s]','',word)
    return word

def train(features):
    model = collections.defaultdict(lambda: 1)
    for f in features:
        model[f] += 1
    return model

with open(r'./BijanKhan Distinct Words.txt', encoding="UTF-8") as fin:
    Nwords = train(normalizer(punctuationRemover(word)) for ln in fin for word in ln.split())
    
alphabet = 'ا ب پ ت ث ج چ ح خ د ذ ر ز  س ش ض  ع غ ف ق ک گ ل م ن و ه ی ء'

def edits1(word):
    splits = [(word[:i], word[i:]) for i in range(len(word) + 1)]
    deletes = [a + b[1:] for a, b in splits if b]
    transposes = [a + b[1] + b[0] + b[2:] for a, b in splits if len(b)>1]
    replaces = [a + c + b[1:] for a, b in splits for c in alphabet if b]
    inserts = [a + c + b for a, b in splits for c in alphabet]
    return set(deletes + transposes + replaces + inserts)

def known_edits2(word):
    return set(e2 for e1 in edits1(word) for e2 in edits1(e1) if e2 in Nwords)

def known(words):
    return set(w for w in words if w in Nwords)

def correct(word):
    candidates = known([word]) or known(edits1(word)) or known_edits2(word) or [word]
    return max(candidates, key=Nwords.get)

while True:
    word = str(input('Please enter a word to see the correction: (enter 0 to end): '))
    if word == '0':
        break
    print('Suggestion --> {}'.format(correct(word)))
    print('=======')

    
