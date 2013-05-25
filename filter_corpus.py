#!/usr/local/bin/pypy

"""
Usage:
    filter_corpus.py <corpus> <wordlist-file> <output-dir>
    
"""
import sys
sys.path.insert(0, '/Library/Python/2.7/site-packages')
import os

from docopt import docopt

arguments = docopt(__doc__)

corpus_dir = arguments['<corpus>']
wordlist = [x.split()[1] for x in open(arguments['<wordlist-file>'])]
output_dir = arguments['<output-dir>']

for basename in os.listdir(corpus_dir):
    fullname = os.path.join(corpus_dir, basename)
    with open(fullname) as f:
        text = f.readline().split()
    filtered = filter(lambda x: x in wordlist, text)
    if len(filtered):
        open(os.path.join(output_dir, basename), 'w').write(
            ' '.join(filtered) + '\n')
