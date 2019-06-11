
Fisher English Training, Part 1:  BBN/WordWave Transcription
============================================================

This distribution contains transcripts and segmentation information
for Fisher conversations produced by BBN in conjunction with WordWave.

The "bbn_orig" directory, like the main "trans" directory, is divided
into groups of 100 calls, where the subdirectory name is simply the
first three digits of the call-ID's in each subset (e.g. "000"
contains data for calls numbered "00001" through "00099", and so on).

Each subset directory contains the following three subdirectories:

    auto-segmented
    originals
    rejected

The directory 'auto-segmented' contains the transcript and
segmentation files produced by BBN and WordWave.  Each conversation
has its own pair of files, for example, the Fisher audio file
"fe_03_00092.sph" has two associated files under "auto-segmented":
"fe_03_00092.ana" and "fe_03_00092.trn".

The ".trn" files are in SNOR format (mono-case text with no syntactic
punctuation).  Each line in these files contains the words for an
utterance followed by the utterance identifier in parentheses.  The
same identifiers are used in the corresponding ".ana" file.  Each line
in the ".ana" file defines the begin and end times for one utterance,
in terms of sample offsets from the start of audio data in the ".sph"
file.  An example line is:

fe_03_00092 -c 1 -t NIST_1A -f 5840-15440 -o fe_03_00092-A-0001

This line indicates that on channel 1 of waveform fe_03_00092.sph,
which is of type NIST_1A, there is an utterance extending from sample
5840 to sample 15440 in the waveform data; "-o fe_03_00092-A-0001"
indicates the name given to this utterance in BBN's system, and the
transcript for this utterance can be found on the line of the
transcript file with the same identifier.  Note that these
segmentations were produced using an automatic algorithm that used
acoustic cues; they do not necessarily reflect sensible linguistic
breakpoints in the text.

The subdirectory 'originals' contains the original transcripts from
WordWave, one per conversation, with a ".txo" extension.  These files
were the input to the process that created the ".trn" and ".ana"
files.  They contain some information that was stripped out in
creating the SNOR format files, such as punctuation, capitalization,
indications of transcriber uncertainty, acronym markers, etc.  They
also contain some mistakes that were fixed later in the process and
they contain some utterances and even complete conversation sides that
were rejected by BBN's automatic post processor.

The subdirectory 'rejected' contains ".ana" and ".trn" files for
rejected portions of the conversations.  These files failed to produce
a good score in BBN's automatic segmentation and filtering procedure,
so it is possible that they contain errors in either the segmentation,
the transcript, or both.  They are included for diagnostic and
research purposes, but it is not expected that they could be used for
acoustic model training without further work.

For questions regarding this data contact Owen Kimball
(okimball@bbn.com) or Chia-lin Kao (ckao@bbn.com)
