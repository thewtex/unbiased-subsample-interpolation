#!/usr/bin/env python

import os
import sys

import numpy as np
from matplotlib import pyplot as plt
from matplotlib import pylab

sys.path.insert( 0, os.path.abspath( os.path.join( __file__, '..', '..', '..', '..' )))
import common.mpl_rc_settings as settings

markers = [ '*', ',' ]
styles  = [ '-', '--' ]
labels  = [ 'TM Phantom', 'Simulation' ]

def plot_it( prefix, postfix, idx ):
    iterations = []
    iterations_std = []
    simplex_deltas = np.arange( 0.1, 1.0, 0.1 )
    for d in simplex_deltas:
        with open( prefix + str(d) + postfix, 'r' ) as f:
            line = f.readline()
            l = line.split()
            iterations.append( float(l[0]) )
            iterations_std.append( 2.0*float( l[1] ) )

    plt.errorbar( simplex_deltas, iterations, iterations_std, markeredgewidth=1.0,
            ms=9.0, alpha=0.5, marker=markers[idx], linestyle=styles[idx],
            label=labels[idx] )
    plt.xlabel( 'Initial simplex offset [samples]' )
    plt.ylabel( 'Number of iterations' )
    plt.xlim( (0.0, 1.0) )

prefix  = 'mean_var_iterations_for_'
postfix = '_simplex_delta_phantom'
plot_it( prefix, postfix, 0 )

prefix  = '../../simulation/simplex_offset/mean_var_iterations_for_'
postfix = '_simplex_delta'
plot_it( prefix, postfix, 1 )

plt.legend( loc='best' )

plt.savefig( '../../../../doc/images/simplex_offset.png' )
plt.savefig( '../../../../doc/images/simplex_offset.eps' )

plt.show()
