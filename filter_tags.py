#!/usr/bin/python

import sys

popular = [x.split()[0] for x in open(sys.argv[2])]
for line in open(sys.argv[1]):
    tokens = line.split()
    filtered = tokens[:1]
    filtered.extend(filter(lambda x: x in popular, tokens[1:]))
    if len(filtered) > 1:
        print ' '.join(filtered)
