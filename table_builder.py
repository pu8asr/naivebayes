#!/usr/local/bin/pypy

"""
Builds frequency distributions over a collection of documents.

Usage:
    table_builder.py <corpus> <popular-tags> <link-to-tag-map> <output-file>

"""

import os
import sys
sys.path.insert(0, '/Library/Python/2.7/site-packages')
import json

from collections import defaultdict
from docopt import docopt

arguments = docopt(__doc__)
corpus_dir = arguments['<corpus>']
popular_tags = dict((x.split()[0], int(x.split()[1]))
                    for x in open(arguments['<popular-tags>']))
link_tag_map = dict()
for l in open(arguments['<link-to-tag-map>']):
    tokens = l.split()
    link_tag_map[tokens[0]] = tokens[1:]
output_file = arguments['<output-file>']

# P(tag)
#label_probdist = DictionaryProbDist(prob_dict=popular_tags, normalize=True)
#label_probdist = UniformProbDist(popular_tags.keys())

# P(word|tag)
dist = defaultdict(lambda: defaultdict(int))
for idx, basename in enumerate(link_tag_map.keys()):
    fullname = os.path.join(corpus_dir, basename)
    try:
        with open(fullname) as f:
            words = f.readline().split()
    except IOError as e:
        continue
    if idx % 1000 == 0:
        print>>sys.stderr, "Processing {0}".format(idx)
    if basename in link_tag_map:
        for tag in link_tag_map[basename]:
            for word in words:
                dist[tag][word] += 1
json.dump(dist, open(output_file, 'wb'))

#feature_probdist = dict()
#for tag in popular_tags.keys():
#    items = dist[tag].items()
#    nwords = sum(x[1] for x in items)
#    for word, freq in items:
#        dist[(tag, word)] = DictionaryProbDist(
#            prob_dict={False: nwords - freq, True: freq}, normalize=True)
#
## Classifier
#classifier = NaiveBayesClassifier(label_probdist, feature_probdist)
