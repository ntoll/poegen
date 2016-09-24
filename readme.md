# London Python Dojo poetry generator

Using Francis T Palgrave's *The Golden Treasury* and the Carnegie Mellon
Pronouncing Dictionary this Python script will make poetry.

Usage:

python poegen.py [*rhyme scheme*, ...]

where *rhyme scheme* is an optional pattern of letters corresponding to rhyming
lines. The default is aabba.

Multiple verses can be specified as multiple arguments.

See http://en.wikipedia.org/wiki/Rhyme_scheme for examples of suitable rhyme
schemes to try.

Example output:

```
$ python poegen.py aabb

A sylvan huntress at my side,
Here the bones of birth have cried
Though others may Her brow adore
Of wishes; and I wish----no more!

$ python poegen.py aabba

Till the ship has almost drank
Into the middle of the plank;
Nor that content, surpassing wealth,
Alas! I have nor hope nor health,
O waly waly up the bank!

$ python poegen.py abab
I dread the rustling of the grass;
Distance, and length;
From hill to hill it seems to pass,
Against thy strength.
```

Your mileage may vary. :-)

Created in about an hour by Dan Pope, Nicholas Tollervey, Hans Bolang and Jon Stutters in November 2013.
