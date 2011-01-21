#!/usr/bin/env python

"""Parse the output of the 'itk-statistics' executable to put it in a format of
one line in an excutable.

Takes data from stdin.  If there are any arguments, it does not append a
newline."""

import sys

mean_line = sys.stdin.readline()
mean = float( mean_line.split()[1] )
sys.stdout.write( str(mean) + ', ' )

sigma_line = sys.stdin.readline()
sigma = float( sigma_line.split()[1] )
sys.stdout.write( str(sigma) + ', ' )

# SNRe
sys.stdout.write( str( abs(mean)/sigma ) )
if len( sys.argv ) == 1:
    sys.stdout.write( '\n' )
else:
    sys.stdout.write( ', ' )
