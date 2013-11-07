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

    return {k: v for k, v in lines_by_rhyme.iteritems() if len(v) > 3}


if __name__ == '__main__':
    rhymedict = CMUDict().word_table

    rhyming_lines = scanLines(rhymedict)

    rhymes = rhyming_lines.values()
    a, b = random.sample(rhymes, 2)

    a_lines = random.sample(a, 3)
    b_lines = random.sample(b, 2)

    last = re.sub(r'\W*$', '', a_lines[-1])
    punc = random.choice('!.?')
    poem = a_lines[:2] + b_lines + [last + punc]
    print '\n'.join(poem)
