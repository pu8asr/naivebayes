#!/usr/local/bin/pypy

"""Given a JSON file containing frequencies of words given tags,
and a file containing popular tags, converts the frequencies to
the logs of their probabilities to avoid this computation repeatedly
in the classifying phase.
"""

import sys
import math
import json

freqfile = sys.argv[1]
popular_tags_file = sys.argv[2]
output_file = sys.argv[3]

popular_tags = dict((x.split()[0], int(x.split()[1]))
                    for x in open(popular_tags_file))
logprob = {}
with open(freqfile, 'rb') as f:
    dist = json.load(f)
    for tag, freqdist in dist.iteritems():
        logprob[tag] = {}
        nwords = sum(freqdist.values())
        for word, freq in freqdist.iteritems():
            # With Laplace smoothing
            logprob[tag].update(
                {word: math.log((freq + 1.0) / (nwords + 100000), 2)})
json.dump(logprob, open(output_file, 'wb'))
