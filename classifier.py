#!/usr/bin/python

"""
Usage:
    classifier.py <p-word-tag> <popular-tags> <infile>

"""

import re
import math
import json

from collections import defaultdict
from docopt import docopt

arguments = docopt(__doc__)
dist = json.load(open(arguments['<p-word-tag>'], 'rb'))
ddist = defaultdict(lambda: defaultdict(int))
for k, v in dist.iteritems():
    for k2, v2 in v.iteritems():
        ddist[k][k2] = v2
popular_tags = dict((x.split()[0], int(x.split()[1]))
                    for x in open(arguments['<popular-tags>']))
infile = arguments['<infile>']
words = []
alnum = r"[a-zA-Z0-9]"
extended_alnum = r"[a-zA-Z0-9.'-]"
punct = r'''[!"#$%&'()*+,\-./:;<=>?@[\\\]^_`{|}~]'''
pattern = '^{0}*({1}{2}*{1}){0}*$'.format(punct, alnum, extended_alnum)
stopwords = set(['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves',
    'you', 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 
    'himself', 'she', 'her', 'hers', 'herself', 'it', 'its', 'itself', 'they', 
    'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 
    'this', 'that', 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 
    'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 
    'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 
    'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 
    'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below',
    'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 
    'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why',
    'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some',
    'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 
    'very', 's', 't', 'can', 'will', 'just', 'don', 'should', 'now'])
with open(infile) as f:
    for word in f.read().strip().split():
        m = re.search(pattern, word)
        if m:
            c_word = m.group(1).lower()
            if len(c_word) > 2 and c_word not in stopwords:
                words.append(c_word)

logprob = defaultdict(float)
alltags = sum(popular_tags.values())
for tag in popular_tags.keys():
    for word in words:
        # With Laplace smoothing
        p = (ddist[tag][word] + 1.0) / (sum(ddist[tag].values()) + 100000)
        logprob[tag] += math.log(p, 2)
    if logprob[tag] < 0:
        logprob[tag] += math.log(popular_tags[tag] * 1.0 / alltags, 2)

logprob = sorted(logprob.items(), key=lambda x: x[1], reverse=True)

for k, v in logprob:
    print k, v
