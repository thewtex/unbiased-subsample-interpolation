#!/usr/bin/env python

import argparse

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np

parser = argparse.ArgumentParser( description='Display a MetaImageFile in a Matplotlib figure.' )

parser.add_argument( 'input_file', type=argparse.FileType('rb') )
parser.add_argument( '-f', '--figure-size', nargs=2, type=float )
parser.add_argument( '-c', '--cmap', type=str, dest='cmap', default='gray' )
parser.add_argument( '-o', '--output-file', type=str )
parser.add_argument( '-p', '--vmin', type=float, default=None )
parser.add_argument( '-q', '--vmax', type=float, default=None )
parser.add_argument( '-l', '--labelsize', type=float )
parser.add_argument( '-i', '--interpolation', type=str, choices=['nearest',
'bilinear', 'bicubic', 'spline16', 'spline36', 'hanning', 'hamming', 'hermite',
'kaiser', 'quadric', 'catrom', 'gaussian', 'bessel', 'mitchell', 'sinc',
'lanczos'] )
args = parser.parse_args()

if args.figure_size:
    plt.figure( 1, figsize=(args.figure_size[0], args.figure_size[1]) )

if args.labelsize:
    mpl.rc( 'axes', labelsize = args.labelsize )
    mpl.rc( 'xtick', labelsize = args.labelsize - 2 )
    mpl.rc( 'ytick', labelsize = args.labelsize - 2 )

l = args.input_file.readline()

element_spacing = [1.0, 1.0]
shape = None
offset = [0.0, 0.0]
while l.split('=')[0].rstrip() != 'ElementDataFile':
    l = args.input_file.readline()
    if l.split('=')[0].rstrip() == 'ElementSpacing':
        element_spacing = [ float(x) for x in l.split('=')[1].rstrip().split() ]
    elif l.split('=')[0].rstrip() == 'DimSize':
        shape = [ int(x) for x in l.split('=')[1].rstrip().split() ]
        shape = tuple( shape[::-1] )
    elif l.split('=')[0].rstrip() == 'Offset':
        offset = [ float(x) for x in l.split('=')[1].rstrip().split() ]

img = np.fromfile( args.input_file, dtype=np.float64 )
args.input_file.close()
img.shape = shape
img = img[9:-9,56:-10]
img = img.transpose()
shape = img.shape

plt.imshow( img,
        cmap=args.cmap,
        aspect=element_spacing[0]/element_spacing[1],
        vmin=args.vmin,
        vmax=args.vmax,
        interpolation=args.interpolation,
        origin='upper',
        extent=(offset[1]*1000, (offset[1] + shape[1]*element_spacing[1])*1000,
             21. + (offset[0] + shape[0]*element_spacing[0])*1000, 21. + offset[0]*1000) )

plt.xlabel( 'Width [mm]' )
plt.ylabel( 'Depth [mm]' )
class cbFormatter( mpl.ticker.ScalarFormatter ):

    def __call__( self, x, pos=None ):
        return '{0}'.format( 100.* x )

cb_formatter = cbFormatter()
cb = plt.colorbar( ticks=[-0.03, -0.02, -0.01, 0.0], format=cb_formatter,
        shrink=0.6, drawedges=False )
cb.outline.set_marker( '' )
cb.set_label( 'Strain Percent' )

if args.output_file:
    plt.savefig( args.output_file )
else:
    plt.show()
