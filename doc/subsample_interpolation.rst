===================================================================
An Approach to Unbiased Subsample Interpolation For Motion Tracking
===================================================================
Matthew M. McCormick\ :sup:`1,2` and Tomy Varghese\ :sup:`1,2`
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

.. highlights::

  :sup:`1`\ Department of Biomedical Engineering

  University of Wisconsin-Madison

  Room 2130 Engineering Centers Building

  1550 Engineering Drive

  Madison, WI 53706-1609

------------------

.. highlights::

  :sup:`2`\ Department of Medical Physics

  University of Wisconsin-Madison

  1111 Highland Ave, Rm 1005

  1550 Engineering Drive

  Madison, WI 53705-2275

-------------------

Correspondence can be sent to matt@mmmccormick.com.


Abstract
========

Accurate subsample displacement estimation is a necessity in ultrasound
elastography because of the small motions that occur and application of a
derivative operation on displacements.  Many commonly used subsample estimation
techniques have a high amount of error because of bias.  In this paper we
examine an unbiased approach subsample displacement estimations that consists of
2D windowed-sinc interpolation with numerical optimization.  We find that a
Welch or Lanczos window with Nelder-Mead simplex optimization are well suited
for this purpose.  The strain signal-to-noise (SNRe) ratio is compared to other
common interpolation methods, and it is found that the SNRe is superior while
still providing reasonable computational performance.


----------------

**Key Words**: Subsample interpolation, strain imaging, motion tracking, sinc
reconstruction.

----------------

1. Introduction
===============

Digital images present challenges in ultrasound motion tracking.  The sampling
rates are barely sufficient to satisfy the Shannon-Nyquist sampling criterion.
For example, a sampling rate of 40 MHz on the Siemens S2000 scanner is very
close to the 20 MHz Nyquist frequency with its 18L6 transducer that purports to
respond to frequencies up to 18 MHz.  In the lateral direction, where resolution
is determined by transducer element spacing, sampling requirements are reduced.
However, the sampling rate is usually an order of magnitude smaller in this
direction.  Furthermore, noise is introduced into the post-deformation signal.
These conditions are a concern when trying to perform ultrasounds strain imaging
where displacement estimates need a precision on the order of micrometers; the
sample spacing in axial direction is only 19 μm with a for a 40 MHz sampling
rate.  Cespedes et al. [Cespedes1995]_ examined the theoretical values for time
delay estimation using cross correlation with parameters from a typical
ultrasound system.  He found the standard deviation due to time quantization was 5.7
ns, which is much larger than the Cramer-Rao Lower Bound (CRLB) for the continuous
case, 0.024 ns.

This subsample delay estimation problem has been studied extensively in 1D in
the sonar and radar fields, where the use of cross-correlation as a similarity
statistic is dominant.  If the signal is approximately narrowband,
quadrature subsample delay techniques can be used [Maskell2002]_. (Tomy: do you
know of other references to use here, possibly something by Kanai?).
Maskell and Woods described a technique where the shift between signals is not
determined by comparing them directly but by comparisons with shifted versions of
a reference signal [Maskell1999]_.  The total delay is then determined to be the difference
between the two delays to the reference signal.

A number of techniques used the fact that phase of the analytic signal's
cross-correlation in the vicinity of the signal shift will have a slope
equivalent to the nominal centroid frequency and zero crossing at the shift
[MarpleJr1999,Pesavento1999]_.  Marple discusses the theory behind this method,
and the scaling that must occur at the DC and Nyquist frenquencies during
calculation that should take place when dealing with discrete signals.
Grennberg and Sandell described a fast subsample delay estimator calculated with
the cross correlation of the delayed signal with the Hilbert transform of the
original signal using an arcsin [Grennberg1994]_.  Other authors used a similar
approach by taking the cross-correlation of base-band analytic signals from both
the original and shifted signal [Pesavento1999,Fromageau2003]_.  The root is
then found with an iterative modified Newton method.  This approach only works
for narrowband signals with small time delays.  For larger time delays,
strategies have to be employed to prevent phase aliasing.  However, if these
approaches can be used, they are advantagous because they are very precise with
minimal computation that can be performed in a single step.  This approach only
works for narrowband signals with small time delays.  In medical ultrasound, the
signal normally only oscillates in the axial direction, so these methods can
only be used to calculate axial displacements.  However, if unconventional
beaming forming strategies are used, phase can also be tracked in the lateral
direction [Basarab2009]_.  Alternatively, a synthetic oscillatory signal can be
generate by taking the inverse Fourier transform of half the transformed signal
[Chen2004]_.  Instead of the more prevalent cross-correlation/Fourier methods,
Viola and Walker have worked on a sum-of-squared error/cubic spline method
[Viola2005,Viola2008]_.  After a cubic spline fit, the problem reduces to
finding the roots of a polynomial whose order is proportional to the number
samples in the fit.

As studied by in [Viola2005]_, a more brute force to determining a more precise
signal shift is to resample the image through interpolation before performing
cross-correlation.  Use of a matched filter during resample may improve the
result [Lai1999].  Instead of resampling and recalculation of the
cross-correlation, curve fitting can be applied.  For example, a parabola
[Boucher1981,Jacovitti1993,Foster1990,Moddemeijer1991,Lai1999]_ or cosine fit
[deJong1990]_ can be used in 1D or an ellipsoid in 2D [Giunta1999]_.  These
methods are computationally efficient and easy to implement, but they suffer
from bias because the underlying signal may not conform to the shape chosen.
[Zahiri-Azar2008,Geiman2000,Jacovitti1993,Moddemeijer1991,Cespedes1995]_.

Curve fitting bias can be avoided by instead using signal reconstruction with
sinc interpolation, which is the maximum likelihood estimator for interpolation
[Cespedes1995,Boucher1981]_.  Cespedes et al. examined the use of 1D sinc
reconstruction to locate the cross-correlation peak, and found that it
significantly out-performs parabolic or cosine interpolation.  Reconstruction is
computationally expensive compared to curve fitting methods, and an optimization
method must be utilized to find the peak location.  Cespedes used a binary
search method to decrease computation times [Cespedes1995]_.

It has also been demonstrated that 2D displacement vector estimates generate
better results than two-pass 1D displacement estimation
[Konofagou1998,Chen2004,Geiman2000,Zahiri-Azar2008]_.  Sumi described an
iterative 2D phase tracking technique [Sumi1999]_, and Ebbini described a similar technique
that iteratively searches for the location where the gradient vectors of the 2D
complex cross correlation are orthogonal, which exists along the zero-phase
contour [Ebbini2006]_.

In this paper, we propose the use of a 2D sinc reconstruction method coupled
with traditional numerical optimization techniques for subsample ultrasound
displacement estimation.  Since parabolic methods remain the most popular method
referenced in the literature and to follow the analysis of Cespedes, we compare
the new method again parabolic and cosine curve fitting.  Performance is
evaluated as the elastographic signal-to-noise ratio (*SNRe*) in phantoms and
simulations.  We examine the optimal sinc-filtering window length and type, and
the computational performance of the Nelder-Mead simplex and a regular step
gradient descent optimizer.

2. Methods
==========

2.1 Algorithm
-------------

In the article by Cespedes et al., a binary search algorithm improved the time
required to localize the subsample 1D cross-correlation peak.  The approach
involves probing the sampled cross-correlation with sinc interpolation.  We
framed this process as a multi-parameter, single-valued cost function numerical
optimization problem.  We applied traditional numerical optimization methods that
have quicker convergence properties than a binary search and can be applied to
multiple parameters.  The cost function to be maximized is the cross-correlation
function.  The parameters to be optimized are the axial and lateral
displacements.

We obtained subsample displacements values with 2D sinc interpolation
[Meijering1999,Yoo2002]_.  The sinc kernel, :math:`K(t)` is given by

.. math:: K(t) =  w(t) sinc(t) = w(t) \frac{\sin(\pi t)}{\pi t} \;\;\;\;\; (Eq.\; 1)

where w(t) is the window function.  We examined the window
functions shown in Table 2.0 [Meijering1999,Yoo2002]_,  Here *m* is the window
radius; the window is non-zero from *-m* to *m*.

Table 2.0 - Sinc window functions
---------------------------------

============= =======================
 Window Name   Expression
------------- -----------------------
 Blackman      :math:`0.42 + 0.50 \cos(\frac{\pi x}{m}) + 0.08 \cos(\frac{2 \pi x}{m})`
 Cosine        :math:`\cos(\frac{\pi x}{2 m})`
 Hamming       :math:`0.54 + 0.46 \cos(\frac{\pi x}{m})`
 Lanczos       :math:`sinc( \frac{\pi x}{m})`
 Welch         :math:`1 - \frac{x^2}{m^2}`
============= =======================

An interpolated normalized cross-correlation value, :math:`XCORR(x,y)` was calculated with
the sampled correlation values across the radius, and the window,

.. math:: XCORR(x,y) = \sum_{i=\lfloor x \rfloor + 1 - m}^{\lfloor x \rfloor + m} \sum_{j=\lfloor y \rfloor + 1 - m}^{\lfloor y \rfloor + m} XCORR_{i,j} K(x-i) K(y-j) \;\;\;\;\; (Eq.\; 2)

In this article, two simple optimization methods were examined, a regular-step
gradient descent and Nelder-Mead simplex (amoeba) optimization.  In the
regular-step gradient descent method, parameters are advanced along the
direction of the negative of the gradient.  The step length is reduced by half
when the sign of the gradient changes [Ibanez2005]_.  The well-known Nelder-Mead
simplex optimization advances a three-point simplex over the optimization space.

We set the initial condition to be the sampled maximum of the normalized
cross-correlation.  The parameter space was the displacement in the axial and
lateral directions defined in fractional samples.  We proceeded with
optimization until reaching convergence defined with a minimum step length with
the regular-step gradient descent method and a parameter tolerance with the
Nelder-Mead simplex method.

The effectiveness of the algorithm was tested on both tissue-mimicking phantom
and simulated ultrasound images.

2.2 Tissue-mimicking phantom
----------------------------

We collected ultrasound radio-frequency (RF) data on a tissue-mimicking (TM)
phantom with a clinical ultrasound scanner, the Siemens S2000 (Siemens
Ultrasound, Mountain View, CA, USA).  The Siemens VFX9-4 linear array transducer
acquired RF data at 40MHz with an excitation frequency of 8.9 MHz and a depth of
5.5 cm.

A 95×95×95 mm, uniform oil-gelatin phantom was placed in a rigid, low-friction basin
and imaged from the top.  Uni-axial, uniform, uncontrained compression was
applied by placing the surface of the tranducer in an acrylic plate.  Slip
boundary conditions were maintained at the interface of the phantom and plate by
ensuring adequate oil was present for lubrication.  Precise deformations in the
directions intended were achieved by a motion with three linear degrees of
freedom, and two rotational degrees of freedom.  A reference image was
collection along with post-deformation images at 0.5%, 1.0%, 3.0%, 5.0%, and
7.0% strain magnitude.  The position of the transducer was rotated and translated to
obtain an independent scattering field, and the set of deformed images were
re-collected.  This process was repeated to obtain 30 independent trials at each
strain magnitude.

2.3 Ultrasound and mechanics simulation
---------------------------------------

2.4 Experimental protocol
-------------------------

3. Results
==========



