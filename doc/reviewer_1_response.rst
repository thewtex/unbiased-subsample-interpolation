===================================================================
An Approach to Unbiased Subsample Interpolation for Motion Tracking
===================================================================
Response to Reviewer 1 Comments
+++++++++++++++++++++++++++++++

We are grateful to the reviewer for their thoughtful and helpful comments.

Response to General Comments
----------------------------

**Comment**

There are several places where the grammar is incorrect in the document.

**Response**

The paper has been reviewed for grammatical correctness.

Response to Specific Comments
-----------------------------

**Comment 1**

Abstract: Lines 4-6: This method is not an unbiased approach since it uses a finite window with a sinc interpolation. Please rephrase to "reduced bias"

**Response 1**

The text has been re-worded per the reviewer's recommendation.

**Comment 2**

Introduction, Paragraph 1, Line 4: Change "underscore" to "underscored".

**Response 2**

This grammatical error has been corrected.

**Comment 3**

Introduction, Paragraph 1, Line 5: What do you mean by "noise is introduced in the post- deformation signal"? Acoustic, thermal and quantization noise is present in the pre- and post-deformation signals. Clarify.

**Response 3**

The intention of the remark was to remind a reader that difficultly in precise displacement estimation is caused by noise in addition to sampling issues.  However, the use of the term "post-deformation" was misleading.  The text now reads:

*Furthermore, acoustic noise also complicates displacement estimation.*

**Comment 4**

Page 7, 2nd line below Eqn (2): Provide reference 

**Response 4**

A reference was added to Chen et al., 2004.

**Comment 5**

Page 8, lines 11-12 and Page 9, line 8: For the axial window lengths (0.5 to 1.3 mm), frequency of 8.9 MHz chosen, assuming a bandwidth of 70% the "bandwidth-time" product is small <3. Explain how you compensate or account for the errors introduced due to the finite window size.

**Response 5**

The following sentence was added to the *Motion tracking algorithm* for clarification:

*Although the time-bandwidth product of the windows used in this algorithm was
small, the multi-resolution techniques along with peak-hopping and signal
stretching avoids errors observed in algorithms without these features.*

**Comment 6**

Page 9, line 8: Provide the bandwidth used. Provide the lateral resolution and the lateral sampling used.

**Response 6**

The following details were added:

*This system had a
full-width-half-maximum fractional bandwidth of 65%. Samples were taken in the
lateral direction every 0.12 mm.*

At this time, data is not readily available to approximate the lateral resolution, but it may be obtained if required.

**Comment 7**

Page 10, lines 6-9: Again, referring to the "bandwidth-time" product, explain how you address the finite window size issue. 
**Response 7**

We defer again to the description of the motion tracking algorithm in section 2.2, which is intentionally designed handle small windows sizes.

**Comment 8**

Page 10, line 10: Change "local" to "lateral".

**Response 8**

This error has been corrected.

**Comment 9**

Page 11, last paragraph: Remove statements and the corresponding results on average time required for convergence.

**Response 9**

The authors believe that it is important to quantify and publish these times
since they contradict the previous publication by Cespedes; the results show
that in a modern computing environment, sinc-interpolation is feasible for
real-time imaging.

**Comment 10**

Page 12, line 4 and Figure 1: Cosine interpolation has been shown by Cespedes [1] to perform better than the parabolic interpolation for the 1-D case. However your results show otherwise. Instead of providing the explanation in the discussion section, provide it here.

**Response 10**

The corresponding explanation in the Discussion has been moved to a better location within the Results.

**Comment 11**

Figure Captions: Correct the grammar.

**Response 11**

The figure captions have been checked for grammar and corrected.

**Comment 12**

Page 12, last paragraph: The images do not show significant improvements. In fact the no-interpolation image(Fig. 3a) is less noisy than the parabolic(Fig. 3b) or cosine interpolation (Fig. 3c). Rephrase. 

**Response 12**

There was a transcriptional error when pasting the images into the document.  Fig. 3d was also used for Fig. 3a.  This has been corrected.

**Comment 13**

Table 3: Remove Table 3 or provide it in terms of order of computations.

**Response**

The table entries are listed in increasing order of computational time.
