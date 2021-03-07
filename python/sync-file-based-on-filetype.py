#!/usr/bin/python
 
# Filename filters, and which folders to send them to:
filters = {
    # Filename  :  Dest Folder
    'dave'      : 'Dave Stuff',
    'bob'       : 'Files For Bob',
    'frank'     : 'Franks Junk',
    }
 
src   = '/Users/Dave/Downloads'
dest  = '/Volumes/Shared'
rsync = 'rsync --times '
 
# ----------------------------------------------------------
 
import os;
import sys;
import subprocess;
 
# Only show progress when we're running in a terminal (and not cron):
if sys.stdout.isatty():
    rsync = rsync + '--progress '
 
for dir, dirs, files in os.walk(src):
    for filename in files:
        if filename.startswith(".") or filename.endswith(".part"):
            continue
        fullpath = os.path.join(dir, filename)
        for filter, destfolder in filters.iteritems():
            if filename.lower().find(filter) >= 0:
                fulldest = os.path.join(dest, destfolder)
                print "Copying '" + filename + "' to folder '" + destfolder + "'"
                cmd = rsync + ' "' + fullpath + '" "' + fulldest + '/."'
                process = subprocess.Popen(cmd, shell=True)
                try:
                    process.wait()
                except KeyboardInterrupt:
                    process.kill()
                    sys.exit(1)
                break
        else:
            print 'Could not find a home for file "' + filename + '"'
