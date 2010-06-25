#!/usr/bin/env python
"""
Convert latex math to images.  Treats the default and ``math`` roles as
inline LaTeX math and the ``math::`` directive as display latex math.

If you include a file which also needs mathhack/imgmathhack preprocessing,
write a name containing ``.mathhack`` in the include directive and it will be
replaced with ``.imgmathhack`` when preprocessed by this script (of course,
you should create both preprocessed versions of the file).

.. note::
    This runs external commands and leaves files after itself!  To reduce
    running time when images are not changed and to reuse images for equal
    fomulas, image names are md5 of the formula (hoping that no collisions
    will happen) and images that already exist are not rebuilt.  You should
    purge the ``imgmath`` subdirectory manually to get rid of unused formulas.

    You'll need:

    - ``klatexformula``
"""

import os, os.path, hashlib
import subprocess

from rolehack import *

class Tex_to_images(object):
    """Feeds math to ``klatexformula``.  Always goes through ppm."""
    def __init__(self, dir='./imgmath', options=['-X', '170', '-f', '#000000'],
                 converter='klatexformula', extension='.png'):
        try:
            os.mkdir(dir)
        except OSError:
            pass
        self.options = options
        self.dir = dir
        self.converter = converter
        self.extension = extension
    def process(self, text):
        """Returns output filename."""
        dir = self.dir
        extension = self.extension
        options = self.options
        converter = self.converter
        fname = hashlib.md5(text).hexdigest()
        fpath = os.path.join(dir, fname)
        if not os.path.exists(fpath + extension):
            next_command = [converter, '-l', text,
                    '-o', fpath + extension ]
            next_command.extend( options )
            subprocess.check_call( next_command )
        return fpath + extension
    def math(self, text):
        text = ' '.join(text.split())
        src = self.process(text)
        return '''\
image:: %(src)s
    :align: middle
    :class: math
    :alt: %(text)s

''' % locals()
    def texdisplay(self, text):
        src = self.process(text)
        return '''\
image:: %(src)s
    :align: center
    :class: texdisplay
    :alt: %(text)s

''' % locals()

child = Tex_to_images()
math = child.math
texdisplay = child.texdisplay

def mangle_include(text):
    return 'include:: ' + text.replace('.mathhack', '.imgmathhack')

#main({'math': math}, math,
     #{'math': texdisplay, 'include': mangle_include})
# do not use the default role because it consumes our other roles
main({'math': math}, None,
     {'math': texdisplay, 'include': mangle_include})
