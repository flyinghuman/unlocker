#!/usr/bin/env python
"""
The MIT License (MIT)

Copyright (c) 2015-2017 Dave Parsons

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the 'Software'), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED 'AS IS', WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""

from __future__ import print_function
import os
import sys
import shutil
import tarfile
import zipfile

try:
    # For Python 3.0 and later
    # noinspection PyCompatibility
    from urllib.request import urlopen
    # noinspection PyCompatibility
    from html.parser import HTMLParser
    # noinspection PyCompatibility
    from urllib.request import urlretrieve
except ImportError:
    # Fall back to Python 2
    # noinspection PyCompatibility
    from urllib2 import urlopen
    # noinspection PyCompatibility
    from HTMLParser import HTMLParser
    # noinspection PyCompatibility
    from urllib import urlretrieve


# Parse the Fusion directory page
class CDSParser(HTMLParser):

    def __init__(self):
        HTMLParser.__init__(self)
        self.reset()
        self.HTMLDATA = []

    def handle_data(self, data):
        # Build a list of numeric data from any element
        if data.find("\n") == -1:
            if data[0].isdigit():
                self.HTMLDATA.append(data)
                self.HTMLDATA.sort(key=lambda s: [int(u) for u in s.split('.')])

    def clean(self):
        self.HTMLDATA = []


def convertpath(path):
    # OS path separator replacement funciton
    return path.replace(os.path.sep, '/')


def main():
    # Check minimal Python version is 2.7
    if sys.version_info < (2, 7):
        sys.stderr.write('You need Python 2.7 or later\n')
        sys.exit(1)

    # Setup url and file paths
    url = 'http://softwareupdate.vmware.com/cds/vmw-desktop/fusion/11.5.0/14634996/core/com.vmware.fusion.zip.tar'
    dest = os.path.dirname(os.path.abspath(__file__))

    # Cleanup working files and folders
    shutil.rmtree(convertpath(dest + '/tools'), True)

    # Re-create the tools folder
    shutil.rmtree(dest + '/tools', True)
    os.mkdir(dest + '/tools')

    # Download the darwin.iso tar file
    print('Retrieving Darwin tools from: ' + url)
    urlretrieve(url, convertpath(dest + '/tools/com.vmware.fusion.zip.tar'))

    # Extract the tar to zip
    tar = tarfile.open(convertpath(dest + '/tools/com.vmware.fusion.zip.tar'), 'r')
    tar.extract('com.vmware.fusion.zip', path=convertpath(dest + '/tools/'))
    tar.close()

    # Extract the iso and sig files from zip
    cdszip = zipfile.ZipFile(convertpath(dest + '/tools/com.vmware.fusion.zip'), 'r')
    cdszip.extract('payload/VMware Fusion.app/Contents/Library/isoimages/darwin.iso', path=convertpath(dest + '/tools/'))
    cdszip.close()

    # Move the iso file to tools folder
    shutil.move(convertpath(dest + '/tools/payload/VMware Fusion.app/Contents/Library/isoimages/darwin.iso'), convertpath(dest + '/tools/darwin.iso'))

    # unzip the darwinPre15.iso
    # Extract the iso file from zip
    cdszip = zipfile.ZipFile(convertpath(dest + '/tools/com.vmware.fusion.zip'), 'r')
    cdszip.extract('payload/VMware Fusion.app/Contents/Library/isoimages/darwinPre15.iso', path=convertpath(dest + '/tools/'))
    cdszip.close()

    # Move the iso file to tools folder
    shutil.move(convertpath(dest + '/tools/payload/VMware Fusion.app/Contents/Library/isoimages/darwinPre15.iso'),
                convertpath(dest + '/tools/darwinPre15.iso'))

    # Cleanup working files and folders
    shutil.rmtree(convertpath(dest + '/tools/payload'), True)
    os.remove(convertpath(dest + '/tools/com.vmware.fusion.zip.tar'))
    os.remove(convertpath(dest + '/tools/com.vmware.fusion.zip'))

if __name__ == '__main__':
    main()
