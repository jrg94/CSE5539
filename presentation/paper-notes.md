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

### 8.1: Introduction

The introduction covers the idea that people are capable of comprehending music
without necessarily separate all the individuals sounds. In other words, they
understand the mixture of sounds. Obviously, we'd like to be able to replicate
that behavior in a computer.

### 8.2: Music Scene Description

The Music Scene Description section introduces the capabilities of untrained music
listeners (i.e. hum melody, clapping on beat, etc.). As a result, a system for
describing music should not consider technical musical details like individual
notes in a chord but rather its overall tone color.

#### 8.2.1 Music Scene Descriptions

The Music Scene Descriptions section introduces three concepts: 

- Local Frequency Structure (Melody Lines vs. Base Lines)
- Local Temporal Structure (Measure Levels)
- Global Music Structure (Repeated/Chorus Sections)

In general, this section covers the history of music scene analysis.
For example, music scene analysis has picked up since the 1990s due
to processing speeds allowing for processor intensive calculations like
fast fourier transforms and other statistical methods. Statistical models
include the Hidden Markov Model and Optima.

#### 8.2.2 Difficulties Associated with Musical Audio Signals

Musical audio signals are complicated and can depend on different factors
such as monaural or stereo (channels), monophonic or polyphonic (number of
sounds), and genre. Granted, stereo signals can be easily reduced to
monaural signals by averaging the channels. That said, generally music signals
are polyphonic, and genre matters because beat structure is more
pronounced in some genres (i.e. pop) than others.

## [REpeating Pattern Extraction Technique (REPET)][2]

At a high level, REPET is a tool for extracting repeating pattern audio from
a musical track. It can be used to separate vocals from a musical track.

[1]: #
[2]: http://music.cs.northwestern.edu/publications/Rafii-Pardo%20-%20REpeating%20Pattern%20Extraction%20Technique%20(REPET)%20A%20Simple%20Method%20for%20Music-Voice%20Separation%20-%20TALSP%202013.pdf
