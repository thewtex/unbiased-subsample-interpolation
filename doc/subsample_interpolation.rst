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
the sonar and radar fields.  
talk about why subsample interpolation is important -- Cespedes


1D xcorr techniques

parametric techniques

bspline technique

rivaz [automatic differention?] brusseau

Cespedes sinc interpolation

