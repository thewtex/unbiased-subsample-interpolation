#!/usr/bin/env python

import os
import sys

import numpy as np
from matplotlib import pyplot as plt
from matplotlib import pylab

sys.path.insert( 0, os.path.abspath( os.path.join( __file__, '..', '..', '..', '..' )))
import common.mpl_rc_settings as settings

def get_snre( radii, snre_record, reg, filename_creator ):
    rec = pylab.csv2rec( filename_creator(1))
    strains = list( set( rec['strain_percent'] ) )
    strains.sort()

    index_is_reg = rec['regularization'] == reg
    mean_snre  = np.ones( (len( radii ), len( strains ))) * 10**-5
    snre_error = np.zeros( (len( radii ), len( strains )))
    for ri, rad in enumerate( radii ):
        rec = pylab.csv2rec( filename_creator(rad))
        strains = list( set( rec['strain_percent'] ) )
        strains.sort()
        index_is_reg = rec['regularization'] == reg
        for si, strain in enumerate( strains ):
            index_is_strain = rec['strain_percent'] == strain
            strain_indices = np.arange( len( rec ) )[ np.nonzero(
                np.logical_and( index_is_strain, index_is_reg ))]
            if snre_record.find( 'lateral' ) == -1:
                strains[si] = strain
            else:
                strains[si] = strain / 2.0
            trials = rec[snre_record][strain_indices]
            if len( trials ) > 0:
                mean_snre[ri, si] = np.mean( trials )
                snre_error[ri,si] = 2*np.std( trials )/np.sqrt( len( trials ))

    return strains, mean_snre, snre_error

class PlotResults( object ):

    def __init__( self ):
        self.fig_num = 1
        self.markers = [ '+' , '*' , ',' , '.' , '1' , '2' , '3' , '4' , 'h' ,
                'o' , 'p' , 's' , 'v' , 'x' , '<' , '>' , 'D' , 'H' , '^' , '_', 'd' ]
        self.iden_index = 0
        self.regs = dict(  {' regularization' : 'Regulation', ' no_regularization' : 'No Regulation' })
        self.snre_records = dict( axial_strain_snre = 'Axial $SNR_e$',
                lateral_strain_snre = 'Lateral $SNR_e$' )
        self.logplot = True

    def plot_snre_curves( self, curve, curve_name, filename_creator ):
        fig_num = 1
        for reg, reg_name in self.regs.iteritems():
            for snre_record, snre_record_name in self.snre_records.iteritems():
                plt.figure( fig_num )
                fig_num += 1
                self._plot_snre_curve( curve, curve_name, reg, reg_name,
                        snre_record, snre_record_name, filename_creator )

    def _plot_snre_curve( self, curve, curve_name, reg, reg_name, snre_record,
            snre_record_name, filename_creator ):

        radii = np.arange( 1, 9 )
        strains, mean_snre, snre_error = get_snre( radii, snre_record, reg,
                filename_creator )

        self.iden_index = iden_index_start
        strains_of_interest_idxs = [1,2]
        for idx in strains_of_interest_idxs:
            plt.errorbar( radii, mean_snre[:,idx], snre_error[:,idx],
                    label=str( curve_name + ' ' + str( strains[idx]) + '% strain' ),
                    marker=self.markers[self.iden_index],
                    markeredgewidth=1.0, markevery=1, ms=9.0, alpha=0.5 )
            plt.xlabel( 'Radius [samples]' )
            plt.ylabel( snre_record_name + ', ' + reg_name )
            #plt.title( str( variable_name ))
            plt.legend( loc='best' )
            if self.logplot:
                plt.gca().set_yscale( 'log' )
            #plt.ylim( (10**-2, 10**2 ) )
            plt.ylim( (10**-0.5, 10**1.1 ) )
            plt.xlim( (0.0, radii[-1]+0.5) )
            self.iden_index += 1



plot_results = PlotResults()
def filename_creator( rad ):
    return 'SNRe_radius' + str( rad ) + '_sim.csv'
iden_index_start = 1
plot_results.plot_snre_curves( 'radius_sim', 'Simulation', filename_creator )
def filename_creator( rad ):
    return '../../phantom/window_length/SNRe_radius' + str( rad ) + '.csv'
iden_index_start = 3
plot_results.plot_snre_curves( 'radius', 'Phantom', filename_creator )


plt.figure( 1 )
plt.savefig( '../../../../doc/images/window_length_regularization_axial.png' )
plt.savefig( '../../../../doc/images/window_length_regularization_axial.eps' )
plt.figure( 2 )
plt.savefig( '../../../../doc/images/window_length_regularization_lateral.png' )
plt.savefig( '../../../../doc/images/window_length_regularization_lateral.eps' )
plt.figure( 3 )
plt.savefig( '../../../../doc/images/window_length_no_regularization_axial.png' )
plt.savefig( '../../../../doc/images/window_length_no_regularization_axial.eps' )
plt.figure( 4 )
plt.savefig( '../../../../doc/images/window_length_no_regularization_lateral.png' )
plt.savefig( '../../../../doc/images/window_length_no_regularization_lateral.eps' )

plt.show()
