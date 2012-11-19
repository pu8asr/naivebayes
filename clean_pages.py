#!/usr/local/bin/pypy

"""
Keeps only sensible words in a collection of documents.

Usage:
    clean_pages.py <pages-dir> <clean-dir> <dirty-dir>

"""

import sys

sys.path.insert(0, '/Library/Python/2.7/site-packages')

import os
import re

from docopt import docopt

arguments = docopt(__doc__)
pages_dir = arguments['<pages-dir>']
clean_dir = arguments['<clean-dir>']
dirty_dir = arguments['<dirty-dir>']
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

os.system('mkdir -p {0}'.format(clean_dir))
os.system('mkdir -p {0}'.format(dirty_dir))
for basename in os.listdir(pages_dir):
    fullname = os.path.join(pages_dir, basename)
    with open(fullname) as f:
        words = f.readline().split()
    alnum = r"[a-zA-Z0-9]"
    extended_alnum = r"[a-zA-Z0-9.'-]"
    punct = r'''[!"#$%&'()*+,\-./:;<=>?@[\\\]^_`{|}~]'''
    pattern = '^{0}*({1}{2}*{1}){0}*$'.format(punct, alnum, extended_alnum)
    clean_words = []
    dirty_words = []
    for word in words:
        m = re.search(pattern, word)
        if m:
            c_word = m.group(1).lower()
            if len(c_word) < 2 or c_word in stopwords:
                dirty_words.append(word)
                continue
            clean_words.append(c_word)
        else:
            dirty_words.append(word)
    with open(os.path.join(clean_dir, basename), 'w') as f2:
        f2.write(' '.join(clean_words))
    with open(os.path.join(dirty_dir, basename), 'w') as f2:
        f2.write(' '.join(dirty_words))
