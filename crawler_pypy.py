#!/usr/local/bin/pypy

help_message="""
Usage: crawler.py [--pick-from-last]
                  <links-file>
                  <tagfile>
                  <pages-directory>
                  <failure-file>

Options:
    --pick-from-last

"""
import sys

sys.path.insert(0, '/Library/Python/2.7/site-packages')

import os
import time
import json
import html2text
import urllib2
import markdown2
import re

from bs4 import BeautifulSoup
from docopt import docopt
from collections import defaultdict

tags = defaultdict(list)

arguments = docopt(help_message)

links_file = arguments['<links-file>']
tagfile = arguments['<tagfile>']
pages_dir = arguments['<pages-directory>']
pick_from_last = arguments['--pick-from-last']
failure_file = arguments['<failure-file>']

tagfile_handler = open(tagfile, 'a')
failure_file_handler = open(failure_file, 'a')

# Pick off from where you last left
last_link_processed = (int(max(
        os.popen("tail -1 {0}".format(tagfile)).read().split()[0],
        os.popen("tail -1 {0}".format(failure_file)).read().split()[0]))
    if pick_from_last else -1)

with open(links_file) as f:
    for idx, line in enumerate(f):
        if idx <= last_link_processed:
            continue
        print>>sys.stderr, idx
        
        # Convert page to plain text
        j = json.loads(line)
        link = j['link']
        try:
            html = urllib2.urlopen(link, timeout=5).read().decode('utf-8')
            md = html2text.html2text(html)
            html = markdown2.markdown(md)
            strings = [re.sub(r'\s+', ' ', x).strip()
                       for x in BeautifulSoup(html).findAll(text=True)]
        except Exception as e:
            if isinstance(e, urllib2.URLError):
                # Check if it's actually a network problem. If so, poll until
                # it's back up.
                while True:
                    try:
                        # Google's IP, to avoid a DNS lookup.
                        response = urllib2.urlopen('http://74.125.113.99',
                                                   timeout=1)
                        break
                    except urllib2.URLError:
                        time.sleep(30)
                        # We'll lose the current document, but not a big deal
                        continue
            failure_file_handler.write("{0} {1}\n".format(idx, e))
            continue
        strings = [x for x in strings if x != '']
        text = ' '.join(strings).encode('ascii', 'ignore')
        
        # Write to file
        with open(os.path.join(pages_dir, str(idx)), 'w') as newfile:
            newfile.write(text)

        # Write to tag file
        if 'tags' in j:
            try:
                tagfile_handler.write('{0} {1}\n'.format(idx,
                    ' '.join(tag['term'].lower() for tag in j['tags'])))
            except Exception as e:
                pass

tagfile_handler.close()
failure_file_handler.close()
