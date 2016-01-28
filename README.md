# Split audio/video streams from single source

This is a quick hack to split a single video file (e.g. of a mixed
interview/observation session) into separate audio-only and video-only
files based on time codes.

# Usage

Given a source audio video file named `input.mov` and a text file containing time codes and section names named `times.txt`:

~~~~
Interview	0:00	4:21
Sibling Harmony	7:06	12:58 complete
Fly Away Blimp	13:47	18:44 complete
Get Tim Home	18:58	21:06 complete
Interview	21:07	24:40
Cannonball!!	24:48	37:36 complete
Excavation Site	37:55	1:02:06	complete
Interview  	1:02:07	1:06:50
Final Countdown	1:07:01	1:32:29	incomplete
Interview	1:32:30	1:42:05
~~~~

run

~~~
$ python split.py input.mov < times.txt
~~~

The output directory `data/output` must exist.

Segments with the name 'Interview' will be split into audio-only files
while other segments will be split into video-only files.

# Input File

The general format for each line of the input file is

~~~~
Section Name    start_time  stop_time    meta_data
~~~~

`start_time` must be in either `HH:MM:SS` or `MM:SS` time
format. `stop_time` must be either in one of those time formats OR it
may be `-` which is taken to mean 'end of the input file.' The
`meta_data` field is currently ignored but could be used for simple
quantitative analysis based on keywords entered for each segment.

# Todo

- Use `argparse` to create a more flexible command interface
- accept command line option to select output directory
- accept command line options to transcode the video/audio into codecs
  different from the input codec.
