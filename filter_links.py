#!/usr/bin/python

from docopt import docopt
import json

help_message="""
Takes a links file and filters out those that have no tag matching tags in the
top tags file.

Usage:
    filter_links.py <top-tags> <links-file> <output-file>
    
"""

arguments = docopt(help_message)
links_file = arguments['<links-file>']
top_tags_file = arguments['<top-tags>']
output_file = arguments['<output-file>']

top_tags = set([x.split()[0] for x in open(top_tags_file).readlines()])
with open(output_file, 'w') as out:
    with open(links_file) as inp:
        for line in inp:
            j = json.loads(line)
            if 'tags' not in j:
                continue
            for tag in j['tags']:
                if tag['term'].lower() in top_tags:
                    out.write(line)
                    break
