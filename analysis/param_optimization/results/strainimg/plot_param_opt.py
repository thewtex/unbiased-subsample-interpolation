#!/usr/bin/env python

# plot the csv file results from param optimization analysis.

import sys

import numpy as np
from matplotlib import pyplot as plt
from matplotlib import pylab

if len( sys.argv ) < 2:
    print('Must pass in path to .csv file.')
    sys.exit(1)

class PlotResults( object ):

    def __init__( self, r, sorted_indices ):
        self.r = r
        self.sorted_indices = sorted_indices
        self.markers = [ '+' , '*' , ',' , '.' , '1' , '2' , '3' , '4' , 'h' ,
                'o' , 'p' , 's' , 'v' , 'x' , '<' , '>' , 'D' , 'H' , '^' , '_', 'd' ]

    def plot_snre( self, record_name, ylabel, index_is_reg, logplot=True ):
        plt.figure()
        variable_values = list( set( self.r[variable_name] ) )
        variable_values.sort()
        strains = list( set( self.r['strain_percent'] ) )
        strains.sort()
        for vi, variable_value in enumerate( variable_values ):
            index_is_vv = self.r[variable_name][self.sorted_indices] == variable_value
            s = np.ones( len( strains )) * 10**-5
            m = np.ones( len( strains )) * 10**-5
            e = np.ones( len( strains )) * 10**-5
            for si, strain in enumerate( strains ):
                index_is_strain = self.r['strain_percent'][self.sorted_indices] == strain
                strain_indices  = self.sorted_indices[np.nonzero(
                    np.logical_and( np.logical_and( index_is_strain, index_is_vv), index_is_reg ))]
                s[si] = strain
                trials = self.r[record_name][strain_indices]
                if len( trials ) > 0:
                    m[si] = np.mean( trials )
                    e[si] = np.std( trials )/np.sqrt( len( trials ))

            print( '\nvariable value: ' + str( variable_value ) )
            print( np.vstack( (s, m, e) ).transpose() )
            plt.errorbar( s, m, e, label=str( variable_value ),
                    marker=self.markers[vi],
                    markeredgewidth=1.0, markevery=1, ms=9.0, alpha=0.5 )
        plt.xlabel( 'Strain Percent' )
        plt.ylabel( ylabel )
        plt.title( str( variable_name ))
        plt.legend( loc='best' )
        if logplot:
            plt.gca().set_yscale( 'log' )
        plt.ylim( (10**-2, 10**2 ) )



r = pylab.csv2rec( sys.argv[1] )
variable_name = r.dtype.names[0]
# I don't think this is actually necessary the way I ended up doing it.
sorted_indices = np.lexsort( (r['strain_percent'], r[variable_name],
    r['regularization'] ) )

regs = set( r['regularization'] )
for reg in regs:
    print( reg )
    index_is_reg = r['regularization'][sorted_indices] == reg

    plot_results = PlotResults( r, sorted_indices )
    print( 'axial strain SNRe' )
    plot_results.plot_snre( 'axial_strain_snre', 'axial $SNR_e$ ' + str( reg ),
            index_is_reg )
    print( 'lateral strain SNRe' )
    plot_results.plot_snre( 'lateral_strain_snre', 'lateral $SNR_e$ ' + str( reg
        ), index_is_reg )

plt.show()
