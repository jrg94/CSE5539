# Presentation Notes

On 4/15, I'll be presenting the following chapter and paper in class:

Goto M. (2006): “Analysis of musical audio signals,” In Wang D.L. & Brown G.J. (eds.):
Computational auditory scene analysis: Principles, algorithms, and applications. IEEE
Press/Wiley, Hoboken NJ, Chapter 8, pp. 251-295.

Rafii Z. and Pardo B. (2013): “REpeating Pattern Extraction Technique (REPET): A simple
method for music/voice separation,” IEEE/ACM Transactions on Audio, Speech, and
Language Processing, vol. 21, pp. 71-82.

Naturally, I'll be using this space to record my notes.

## [Analysis of Musical Audio Signals][1]

This chapter is broken up into sections, so I'll summarize them separately.

### 8.1: Introduction (251 - 252)

The introduction covers the idea that people are capable of comprehending music
without necessarily separate all the individuals sounds. In other words, they
understand the mixture of sounds. Obviously, we'd like to be able to replicate
that behavior in a computer.

### 8.2: Music Scene Description (252 - 256)

The Music Scene Description section introduces the capabilities of untrained music
listeners (i.e. hum melody, clapping on beat, etc.). As a result, a system for
describing music should not consider technical musical details like individual
notes in a chord but rather its overall tone color.

#### 8.2.1 Music Scene Descriptions (253 - 255)

The Music Scene Descriptions section introduces three concepts: 

- Local Frequency Structure (Melody Lines vs. Base Lines)
- Local Temporal Structure (Measure Levels)
- Global Music Structure (Repeated/Chorus Sections)

In general, this section covers the history of music scene analysis.
For example, music scene analysis has picked up since the 1990s due
to processing speeds allowing for processor intensive calculations like
fast fourier transforms and other statistical methods. Statistical models
include the Hidden Markov Model and Optima.

#### 8.2.2 Difficulties Associated with Musical Audio Signals (255 - 256)

Musical audio signals are complicated and can depend on different factors
such as monaural or stereo (channels), monophonic or polyphonic (number of
sounds), and genre. Granted, stereo signals can be easily reduced to
monaural signals by averaging the channels. That said, generally music signals
are polyphonic, and genre matters because beat structure is more
pronounced in some genres (i.e. pop) than others.

### 8.3 Estimating Melody and Base Lines (256 - 266)

This sections opens up with some application domains for estimating melody
and base lines such as retreiving a musical piece by humming or automatic
production of accompaniment tracks for karaoke.

Later, the section discusses challenges with using current techniques like
F0 estimation which depends on single tones that lack periodic noise. Even
special F0 estimation methods fail due to the smearing of harmonics.

Fortunately, F0 estimation in music was first achieved in 1999 using PreFEst.
PreFEst works by estimating F0 from the most predominant harmonic structure
using a probability density function (PDF). Unfortunately, I struggled to
grasp exactly how it works from all the signal processing jargon. Luckily,
this section claims that the process will be explained in more detail. That
said, the basic model works in three parts:

1. Front end: frequency analysis
2. Core: predominant F0 estimation
3. Back end: temporal continuity evaluation

Based on this model, melody and bass lines can be extracted using frequency-
range limitations during core processing.

#### 8.3.1 PreFEst-front-end: Forming the Observed Probability Density Function (258)

The PDF is generated by passing the music signal through a multirate filter
bank and extracting two frequency components via two band pass filters: 
261.6-4186 Hz for melody and 32.7-261.6 Hz for bass line. From there,
the sets of components are represented as an observed PDF. 

#### 8.3.2 PreFEst-core: Estimating the F0's Probability Density Function (258)

Using the observed PDFs, the core forms a PDF of the F0. I'll need to reread this
section to really get it.

##### 8.3.2.1 Weighted-Mixture Model of Adaptive Tone Models (258 - 260)

An observed PDF is assumed to be generated from a model which is a weighted
mixture of all possible tone models (whatever that means). 

##### 8.3.2.2 Introducing a Prior Distribution (260 - 261)

How to create a prior distribution?

##### 8.3.2.3 MAP Estimation Using the EM Algorithm (261 - 262)

Apparently, it's too hard to perform an integral, so we use
some Expectation-Maximization algorithm to compute MAP
estimates from incomplete observed data. 

Apparently, this complex mathematical solution is better than
comb-filter based and autocorrelation-based multiple F0
estimation methods because they cannot separate overlapping
frequency components. 

#### 8.3.3 PreFEst-back-end: Sequential F0 Tracking by Multiple-Agent Architecture (262 - 263)

F0 is tracked over time. The most predominant and stable F0 is then selected. 

#### 8.3.4 Other Methods (263 - 266)

PreFEst is great, but it has drawbacks--namely, bias can be including in detection.

Paiva, Mendes, and Cardoso implemented a solution based on human anatomy that can
generate MIDI output rather than an F0 trajectory. The solution leverages correlograms
and forms temporal trajectories of F0 candidates. These candidates are quantized to
the closest MIDI note numbers and some analysis is done to remove transient notes
and harmonics. Finally, the best sequence is chosen based on some heuristic. 

Meanwhile, Marolt leverages PreFEst core to estimate F0 candidates, but uses
spectral modeling synthese (SMS) on the front end. The advantage to this method
is the ability to identify melody fragments which can be clustered into a 
melody line. Clustering is accomplished using Gaussian Mixture Models (GMMs)
based on dominance, pitch, loudness, pitch stability, and onset steepness. 

For classical music, Eggink and Brown developed a method of detecting
melody lines using various knowledge sources for prediction. Knowledge
sources include local knowledge (i.e. instrument recognition) and temporal 
knowledge. I'll need to read this again to get a good understanding.

For vocal music, Li and Wang extend F0 estimation from noisy speech techniques.
Music signals are sent through a 128 gammatone filterbank and split by a
frequency of 800 Hz. Then some analysis is done to extract the melody line.

Finally, Hainsworth and Macleod came up with a method for detecting base lines.
First, they extract onset times of notes below 200 Hz. Then, they perform some 
F0 analysis and track the results over time using comb-filter like analysis.
The results are then cleaned up.

### 8.4 Estimating Beat Structure (267 - 275)

Once again, this section kicks off with some applications of estimating beat
structure such as music-synchronized computer graphics, stage-lighting control, 
and human-computer improvisation in live ensembles.

Next, the section lists a ton of historical work that went into tracking beat
in MIDI and CD recordings over the years. 

After that, the section defines what hierarchical beat structure is: quarter note
and bar line tracking. Quarter notes are tracked through period and phase
and measures are track through sequences of quarter notes.

Finally, they introduce the challenges of tracking beats in CD musics. Namely:

1. Estimating the period and phase by using cues in audio singlas
    - Current techniques fail in in polyphonic audio signals
2. Dealing with ambiguity of interpretation
    - Multiple interpretations of beats are possibles
3. Using musical knowledge to make musical decisions
    - Musical knowledge allows for reduction of ambiguity

#### 8.4.1 Estimating Period and Phase (268 - 270)

The basic idea is to detect onset times and use them as cues for estimating
the period and phase. The onset itself corresponds to the beat and the distance
between beats constitutes the phase.

Of course, this is overly simplistic as onset could indicate eight or sixteenth
notes which are fractions of the beat. A better solution is to run an autocorrelation
over the onset times and check the peaks of the result.

For audio-based tracking, it's important to split the frequency of the track into
bands and determine periodicity in those respective bands. One solution is to 
perform the method above and combine the results using a weighted sum. 

Other methods avoid onset altogether and instead apply a set of comb-filter
resonators (whatever those are) to the degrees of musical accentuation
of various subbands. 

With the beat period estimated, it's helpful to estimate the phase. 

#### 8.4.2 Dealing with Ambiguity (270 - 271)

The general method for dealing with ambiguity is to track multiple hypotheses.
The most reliable hypotheses then wins out.

It's also possible to use probabilistic models to solve ambiguity.

#### 8.4.3 Using Musical Knowledge (271 - 275)

It's possible to use prior music knowledge when computing the reliability
of a hypothesis. Some folks used knowledge about chord progressions while
others used knowledge about temporal relationships in hierarchical beat
structures.

Unfortunately, it's challenging to use drum patterns and chord changes if 
you don't have the beat, so some solutions use both bottom up and top down
approaches simulataneously. The bottom up portion of the system estimates
beats using onset while the top up portion of the system uses the hypothetical
beats to detect chord changes. Using the chord changes and drum patterns,
higher level information can be extracted like measure numbers.

This section contains a lot of excellend figures for explanation purposes.

### 8.5 Estimating Chorus Sections and Repeated Sections (275 - 286)

In this section, the authors explain what chorus is and why it's important.
They also describe applications like music browsers and retrieval systems.

Chorus sections are extracted by recognizing that they're usually the most
repeated sections of a song. Naturally, the author describes many works
that have done exactly that.

Of course, there are challenges:

1. Extracting acoustic features and calculating their similarity
2. Finding repeated sections
3. Grouping repeated sections
4. Detecting modulated repetition
5. Selecting chorus sections

The remaining sections basically cover RefraiD (Refrain Detection method). RefraiD
leverages a 12-dimensional feature vector called a chroma vector which encapsulates
Each element of the vector represents one of 12 pitch classes. 

To account for key changes, the vectors are shifted for all possible keys and differences
are calculated between all shifted vectors.

RefraiD solves all 5 problems.

#### 8.5.1 Extracting Acoustic Features and Calculating Their Similarities (278 - 281)

Highlights studies which used same features.

##### 8.5.1.1 Pitch Feature: Chroma Vector (278 - 280)

A chroma vector is based on the concept of a chroma thanks
to Shephard's helix representation of musical pitch perception.
Essentially, octaves are meaningless. They correspond to height of
the helix. The circular location gives the actual pitch. 

Chroma vectors are great for detecing chords and harmony.

Again, lots of math here, but the images are good.

##### 8.5.1.2 Timbral Feature: MFCC and Dynamic Features (280)

Supervised learning can be used to capture what chroma vectors can't:
dynamic features like texture.

##### 8.5.1.3 Calculation Similarity (280 - 281)

Calculating similiarity of two vectors is just a matter of calculating
distance. Euclidean distance is fine, but don't forget to normalize.

In RefrainD, the distance function is wild.

#### 8.5.2 Finding Repeating Sections (281 - 282)

Repeated sections can be found using a similarity matrix and a
time-lag triangle. 

The RefraiD method gets all horizontal lines in the time-lag triangle,
then does some other math...

Of course, there are other approaches. 

#### 8.5.3 Grouping Repeating Sections (282 - 284)

Unfortunately, each line segment in the time-lag triangle only represents
pairs of repeated sections. To group them, RefraiD looks for similar line
segments and recomputes hidden section using topdown information from
discovered sections.

#### 8.5.4 Detecting Modulated Repetition (284 - 285)

Unfortunately, key changes add an element of complexity to similarity detection.
Similarity can then be extended for all 12 keys. Grouping occurs for same sections.

#### 8.5.5 Selecting Chorus Sections (285)

Detecting chorus sections requires looking at the groups and determining which one
had the most and longest line segments. Of course, as an added heuristic, RefraiD
limits chorus detection to:

1. length (7.7 to 4 seconds)
2. chorus is at end of repeated section
3. chorus contains repeated subsections

#### 8.5.6 Other Methods (285 - 286)

1. Using HMMs and clustering
2. Use beat tracking
3. Short frames (100 ms)

Also:

1. Dynamic programming and iterative greedy algorithms
2. Supervised learning
3. etc. etc. etc.

### 8.6 Discussions and Conclusions (286 - 289)

Recap.

#### 8.6.1 Importance (286 - 287)

Let's understand music signals from a human-like viewpoint.
Music ausio signal research is complementary to speech recognition
research.

Music is now everywhere! It would be nice to have utilities for working
with music for the average user (i.e. being able to search for similar
sounding songs, being able to automatically classify music).

#### 8.6.2 Evaluation Issues (287 - 288)

Evaluation is challenging as there isn't a large database of music files
for public consumption with proper metadata. Luckily, there are some
databases. 

#### 8.6.3 Future Directions (288 - 289)

- Recognizing instruments in music
- MIDI processing
- etc.

## [REpeating Pattern Extraction Technique (REPET)][2]

At a high level, REPET is a tool for extracting repeating pattern audio from
a musical track. It can be used to separate vocals from a musical track.

[1]: #
[2]: http://music.cs.northwestern.edu/publications/Rafii-Pardo%20-%20REpeating%20Pattern%20Extraction%20Technique%20(REPET)%20A%20Simple%20Method%20for%20Music-Voice%20Separation%20-%20TALSP%202013.pdf
