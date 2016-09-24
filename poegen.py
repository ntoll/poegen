"""
Generates poetry on demand given a rhyming scheme and Palgraves Golden
Treasury.

Created by Dan Pope, Nicholas Tollervey, Hans Bolang and Jon Stutters.
"""
import sys
import re
import random
from collections import defaultdict, Counter


PRONUNCIATION_DICT = 'cmudict.0.7a'
POEM_LINES = 'lines.txt'
PHONEME_TABLE = 'cmudict.0.7a.phones'


def stripped_lines(fname):
    """
    Iterate over the stripped, non-blank lines of fname.
    """
    with open(fname) as f:
        for l in f:
            l = l.strip()
            if l:
                yield l


def load_pronounciation_dict():
    """
    Load a dictionary of word -> last sylable phonemes.
    """
    phones = CMUPhones()
    word_table = {}
    for l in stripped_lines(PRONUNCIATION_DICT):
        l = re.sub(r'\d', '', l)  # Strip phomeme stresses
        toks = l.strip().split()
        word = toks[0]
        phonemes = toks[:0:-1]
        curphon = []
        for p in phonemes:
            curphon.append(p)
            if phones.is_vowel(p):
                break
        word_table[word] = tuple(curphon)
    return word_table


class CMUPhones(object):
    """
    A table of phoneme types.
    """
    def __init__(self):
        self.read_phones()

    def read_phones(self):
        self.phones = dict(l.split() for l in stripped_lines(PHONEME_TABLE))

    def is_vowel(self, c):
        return self.phones.get(c) == 'vowel'


def last_word(line):
    """
    Return the last word in a line (stripping punctuation).

    Raise ValueError if the last word cannot be identified.
    """
    mo = re.search(r"([\w']+)\W*$", line)
    if mo:
        w = mo.group(1)
        w = re.sub(r"'d$", 'ed', w)  # expand old english contraction of -ed
        return w.upper()
    raise ValueError("No word in line.")


def load_rhymes():
    """
    Collect poem lines into groups of lines that all rhyme.
    """
    rhymedict = load_pronounciation_dict()
    lines_by_rhyme = defaultdict(list)
    for l in stripped_lines(POEM_LINES):
        try:
            rhyme = rhymedict[last_word(l)]
        except (KeyError, ValueError):
            continue

        lines_by_rhyme[rhyme].append(l)

    return [ls for ls in lines_by_rhyme.values() if len(ls) > 1]


def terminate_poem(poem):
    """
    Given a list of poem lines, fix the punctuation of the last line.

    Removes any non-word characters and substitutes a random sentence
    terminator - ., ! or ?.
    """
    last = re.sub(r'\W*$', '', poem[-1])
    punc = random.choice('!.?')
    return poem[:-1] + [last + punc]


def build_poem(rhyme_scheme, rhymes):
    """
    Build a poem given a rhymne scheme, eg aabbcaa.

    Spaces are translated to paragraph breaks.
    """
    groups = Counter(rhyme_scheme.replace(' ', ''))

    lines = {}

    # Choose the lines to use
    for k, c in groups.items():
        ls = random.choice([v for v in rhymes if len(v) > c])
        lines[k] = random.sample(ls, c)
        rhymes.remove(ls)

    # Build the poem
    poem = []
    for k in rhyme_scheme:
        if k == ' ':
            if poem:
                poem = terminate_poem(poem) + ['']
        else:
            poem.append(lines[k].pop())
    return terminate_poem(poem)


if __name__ == '__main__':
    rhyme_scheme = ' '.join(sys.argv[1:]) or 'aabba'
    rhymes = load_rhymes()
    poem = build_poem(rhyme_scheme, rhymes)
    print('\n'.join(poem))
