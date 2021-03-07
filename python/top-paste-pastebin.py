#!/usr/bin/env python
"""
pasteget.py -- top paste retrieval script

This script retrieves the top 20 pastes for the last 48 hours from pastebin.com.

Usage: python pasteget.py

Dependencies: BeautifulSoup

Configuration: The assumption is that you have a folder called
'pastes' in your home directory (not sure how this affects Windows, but it will
work on any *nix or Linux. You can change the default base path for pastes by
editing the 'base' global variable. Also, the script only has support for some
file extensions by default; you can add something else you'd like by editing
the 'extensions' global variables. You can also change the number of pastes
you'd like by editing the global variable 'top_n'.

Statistics: the script (by default) downloads the top 20 pastes from the past
48 hours. Downloading 20 pastes, based on my tests, took up 641 KB of space
(so a little more than that in bandwidth). On my machine, the script also
takes about 2.5 mins to run, mainly due to time spent waiting so that pastebin
doesn't reject my requests (I have to wait about 7 seconds after downloading
each paste, or else some requests might return a 'Too many requests, slow down'
message.

License: MIT License, see the license in the repo

Author: Rafe Kettler, April 6, 2011

Additional notice: I'm not responsible for anything that happens when you use
the script. If you end up downloading something questionable, that's on you.
"""

import os
import time
from urllib2 import urlopen
from BeautifulSoup import BeautifulSoup

####################################################
# Global configuration variables
####################################################
# base path for pastes to be stored
base = os.path.join(os.environ["HOME"], "pastes")
# number of pastes to download
top_n = 20
# recognized extensions
extensions = {'None':'',
              'C':'.c',
              'C++':'.cpp',
              'PHP':'.php',
              'Python':'.py',
              'JavaScript':'.js',
              'ASM (NASM)':'.asm',
              'Java':'.java',
              'C#':'.cs',
              'SQL':'.sql',
              'Perl':'.pl',
              'HTML':'.html',
              'Lisp':'.lisp',
              'Bash':'.sh',
              'CSS':'.css',
              'Ruby':'.rb'}

trends = urlopen("http://pastebin.com/trends")
parser = BeautifulSoup(trends)

def parse():
    paste_hashes = {}
    # First tr is heading, we only want the first 20 pastes
    top_pastes_tags = parser.findAll('tr')[1:top_n + 1]
    for paste in top_pastes_tags:
        tds = paste.findAll('td')
        link = tds[0].find('a')['href'] # Link is first td
        lang = tds[3].text
        # link[1:] is link w/o leading slash
        paste_hashes[link[1:]] = lang
    return paste_hashes

def make_folder():
    title = "top_from_%s" % time.strftime("%m_%d_%Y")
    # See global variable base
    path = os.path.join(base, title)
    os.mkdir(path)
    return path
    

def get_pastes(pastes, path):
    for paste, lang in pastes.items():
        try:
            ext = extensions[lang]
        except KeyError:
            # Not in the dict, no worries
            ext = ''
        with open(os.path.join(path, paste + ext), 'w') as f:
            text = urlopen("http://pastebin.com/raw.php?i=" + paste).read()
            f.write(text)
        # necessary to beat request limits
        time.sleep(7)

if __name__ == '__main__':
    pastes = parse()
    path = make_folder()
    get_pastes(pastes, path)
    
