#!/usr/bin/env python

from sys import stdin, argv
from datetime import datetime
import re
import subprocess as sp
import os.path as path

#audio_codec = 'libvorbis'
#audio_options = ['-qscale:a', '5']
audio_codec = 'copy'
audio_options = []
audio_ext = 'mp4'
#video_codec = 'libvpx'
#video_options = ['-crf', '10', '-b:v', '7M']
video_codec = 'copy'
video_options = []
video_ext = 'mov'
output_dir = 'data/output'
input_file = argv[1]
slices = []

rslice = re.compile(r'([^0-9]+)\s+([0-9:]+)\s+((?:[0-9:]+|-))(?:\s+([a-z]+))?')

cmd = ['ffmpeg', '-y', '-threads', '8', '-i', input_file]

base_name, ext = path.basename(input_file).split('.')

def parse_time(time):
    t = None
    try:
        t = datetime.strptime(time, '%H:%M:%S')
    except ValueError:
        t = datetime.strptime(time, '%M:%S')
    return t
    
def duration(start_time, stop_time):
    s1 = parse_time(start_time)
    s2 = parse_time(stop_time)
    duration = s2 - s1
    return duration

def stream_slice_args(start_time, stop_time):
    args = ['-ss', start_time]
    if stop_time is not None and not stop_time == '-':
        args = args + ['-t', str(duration(start_time,stop_time))]
    return args

class FileNamer():
    def __init__(self, template, **kwargs):
        self._count = kwargs.pop('count', 0)
        self.template = template
        self.auto_increment = kwargs.pop('auto_increment', True)
        
    def name(self, *args):
        _name = self.template.format(*args, count=self._count)
        if self.auto_increment:
            self._count = self._count + 1
        print("generating new name: {}".format(_name))
        return _name

    def increment(self):
        self._count = self._count + 1

    @property
    def count(self):
        return self._count
    
interview_namer = FileNamer('{}_interview_{count}.{}', count=1)
puzzle_namer = FileNamer('{}_{}_{count}.{}', auto_increment=False)

def line_to_cmd(line):
    cmd = []
    m = rslice.search(line)
    print('match groups: {}'.format(m.groups()))
    if m:
        status = None
        puzzle_name, start_time, stop_time = m.group(1).strip(), m.group(2), m.group(3)
        if m.group(4):
            status = m.group(4)
        if puzzle_name == 'Interview':
            cmd = cmd \
              + ['-vn', '-c:a', audio_codec] \
              + audio_options \
              + stream_slice_args(start_time, stop_time)
            cmd.append( path.join(output_dir, interview_namer.name(base_name, audio_ext)) )
            puzzle_namer.increment()
        else:
            cmd = cmd + ['-an', '-c:v', video_codec] \
              + video_options \
              + stream_slice_args(start_time, stop_time)
            cmd.append( path.join(output_dir, puzzle_namer.name(base_name, puzzle_name, video_ext)) )
    else:
        print('could not parse: {}'.format(line))
    return cmd


#commands = [ line_to_cmd(line) for line in stdin ]

for line in stdin:
    cmd = cmd + line_to_cmd(line)
    print(cmd)
    
sp.call(cmd)
