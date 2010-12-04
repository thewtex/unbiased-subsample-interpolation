===================================================================
An Approach to Unbiased Subsample Interpolation For Motion Tracking
===================================================================

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

Introduction
============

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

As studied by in [Viola2005], a more brute force to determining a more precise
signal shift is to resample the image through interpolation before performing
cross-correlation.  Use of a matched filter during resample may improve the
result [Lai1999].  Instead of resampling and recalculation of the
cross-correlation, curve fitting can be applied.  For example, a parabola
[Boucher1981,Jacovitti1993,Foster1990,Moddemeijer1991,Lai1999]_ or cosine fit
[deJong1990]_ can be used in 1D or an ellipsoid in 2D [Giunta1999]_.  These
methods are computationally efficient and easy to implement, but they suffer
from bias because the underlying signal may not conform to the shape chosen.
[Zahiri-Azar2008,Geiman2000,Jacovitti1993,Moddemeijer1991,Cespedes1995]_.

Cespedes sinc interpolation

It has also been demonstrated that 2D displacement vector estimates generate
better results than two-pass 1D displacement estimation
[Konofagou1998,Chen2004,Geiman2000,Zahiri-Azar2008]_.  Sumi described an
iterative 2D phase tracking technique [Sumi1999]_, and Ebbini described a similar technique
that iteratively searches for the location where the gradient vectors of the 2D
complex cross correlation are orthogonal, which exists along the zero-phase
contour [Ebbini2006]_.

rivaz [automatic differention?] brusseau

