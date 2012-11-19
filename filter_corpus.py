#!/usr/local/bin/pypy

import sys
import os

corpus_dir = sys.argv[1]
output_dir = sys.argv[3]
wordlist_file = sys.argv[2]
wordlist = [x.split()[1] for x in open(wordlist_file)]

for basename in os.listdir(corpus_dir):
    fullname = os.path.join(corpus_dir, basename)
    with open(fullname) as f:
        text = f.readline().split()
    filtered = filter(lambda x: x in wordlist, text)
    if len(filtered):
        open(os.path.join(output_dir, basename), 'w').write(
            ' '.join(filtered) + '\n')
