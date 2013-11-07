import re
import random
from collections import defaultdict


def make_limerick():
    pass

def rhyming_pair():
    """CMU pronouncing dictionary"""
    pass

def random_place():
    pass

def random_thing():
    pass

class CMUDict:
    def __init__(self):
        self.cmup = CMUPhones()
        self.read_from_file()

    def read_from_file(self):
        with open('cmudict.0.7a') as f:
            all_phonemes = []
            self.word_table = {}
            for l in f:
                l = l.strip()
                l = re.sub(r'\d', '', l)
                toks = l.strip().split()
                word = toks[0]
                phonemes = toks[1:]
                phonemes.reverse()
                curphon = []
                for p in phonemes:
                    curphon.append(p)
                    if self.cmup.is_vowel(p):
                        break
                self.word_table[word] = tuple(curphon)


class CMUPhones:
    def __init__(self):
        self.read_phones()

    def read_phones(self):
        with open('cmudict.0.7a.phones') as f:
            self.phones = dict(l.strip().split() for l in f)

    def is_vowel(self, c):
        return self.phones.get(c) == 'vowel'


def scanLines(rhymedict):
    lines_by_rhyme = defaultdict(list)
    with open('lines.txt') as f:
        for l in f:
            l = l.strip()
            mo = re.search(r"([\w'-]+)\W*$", l)
            if mo:
                last_word = mo.group(1)
                try:
                    rhyme = rhymedict[last_word.upper()]
                except KeyError:
                    continue

                lines_by_rhyme[rhyme].append(l)

    return {k: v for k, v in lines_by_rhyme.iteritems() if len(v) > 1}


if __name__ == '__main__':
    import sys

    try:
        rhyming = sys.argv[1]
    except IndexError:
        rhyming = 'aabba'

    rhymedict = CMUDict().word_table

    rhyming_lines = scanLines(rhymedict)

    rhymes = rhyming_lines.values()

    ca = rhyming.count('a')
    cb = rhyming.count('b')
    a = random.choice([v for v in rhymes if len(v) > ca])
    rhymes.remove(a)
    b = random.choice([v for v in rhymes if len(v) > cb])

    a_lines = random.sample(a, ca)
    b_lines = random.sample(b, cb)

    poem = []
    for c in rhyming:
        poem.append(a_lines.pop(0) if c == 'a' else b_lines.pop(0))

    last = re.sub(r'\W*$', '', poem[-1])
    punc = random.choice('!.?')
    poem = poem[:-1] + [last + punc]
    print '\n'.join(poem)
