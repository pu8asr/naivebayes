#!/usr/bin/python

import json
import sys

delicious = sys.argv[1]
freq = {}
with open(delicious) as f:
    for line in f:
        j = json.loads(line)
        if 'tags' not in j:
            continue
        for tag in j['tags']:
            term = tag['term'].lower()
            freq[term] = freq.get(term, 0) + 1

for item in sorted(freq.items(), key=lambda x: x[1], reverse=True):
    try:
        print item[0], item[1]
    except:
        pass
