#!/usr/bin/env python

import os
import sys
import re
import argparse
import subprocess

ffmpeg = subprocess.check_output(["which", "ffmpeg"]).decode("utf-8").rstrip('\n')

# Create a parser
parser = argparse.ArgumentParser(description='Trim and convert video to mp3')

parser.add_argument('input', nargs=1, type=str,
                   help='Input video file')
parser.add_argument('-b', '--bitrate', nargs=1, type=str,
                   help='Audio bitrate (default: 196k)')
parser.add_argument('-s', '--start', nargs=1, type=str,
                   help='Start time (default: 00:00:00)')               
parser.add_argument('-e', '--end', nargs=1, type=str,
                   help='End time (default = end of input)')
parser.add_argument('-v', '--video', nargs=1, type=str,
                   help='Output trimed video file (y/n, default is y')
parser.add_argument('output', nargs='?', type=str,
                   help='Output file name (default = audio.mp3)')

args = parser.parse_args()
print(args)

input_name = 'output'
# Input
if os.path.exists(args.input[0]):
    ifile = args.input[0]
    base = os.path.basename(args.input[0])
    name_list = os.path.splitext(base)
    input_name = ''.join(name_list[:-1])
else:
    print(f'{args.input[0]} does not exist!')

# Bitrate
bitrate = '196k'
if args.bitrate:
    digits = re.findall(r'\d+', args.bitrate[0])
    bitrate = ''.join(digits) + 'k'

# Start time
ts = '00:00:00'
if args.start:
    digits = re.findall(r'\d+', args.start[0])
    digits = ''.join(digits)
    digits = '000000' + digits
    ts = digits[-6:-4] + ':' + digits[-4:-2] + ':' + digits[-2:] 

# End time
te = ''
if args.end:
    digits = re.findall(r'\d+', args.end[0])
    digits = ''.join(digits)
    digits = '000000' + digits
    te = digits[-6:-4] + ':' + digits[-4:-2] + ':' + digits[-2:] 

print(f'Start time: {ts}')
print(f'End   time: {te}')

if int(te.replace(':', '')) <= int(ts.replace(':', '')):
    sys.exit(f'Error: start_time > end time!')

# Output video or not
output_video = True
if args.video:
    choice = args.video[0].lower()
    if choice in ['n', 'no']:
        output_video = False
    elif choice not in ['y', 'yes']:
        sys.exit(f'Error: invalid -v option - {args.video[0]}! \n       Choose y/n')

# Output file name
te_name = te.lstrip('0:')
ts_name = ts[-len(te_name):]
fname = f'{input_name}_{ts_name}-{te_name}'

if args.output:
    fname = args.output.rstrip('.mp3')

ofile = fname+'.mp3'
print(ofile)

ffmpeg = subprocess.check_output(["which", "ffmpeg"]).decode("utf-8").rstrip('\n')

def trim_video(ffmpeg, ifile, ofile, ts, te):

    commands_list = [
        ffmpeg,
        "-i",
        ifile,
        "-ss",
        ts,
        "-c", 
        "copy", 
        ofile
        ]

    if te:
        commands_list.insert(7, "-to")
        commands_list.insert(8, te)
    
    return commands_list

def convert_mp3(ffmpeg, ifile, ofile, bitrate):

    commands_list = [
        ffmpeg,
        "-i",
        ifile,
        "-b:a",
        bitrate,
        ofile
        ]

    return commands_list


# Trim video
vfile = fname + '.mp4'
commands_list = trim_video(ffmpeg, ifile, vfile, ts, te)

print(commands_list)
if subprocess.run(commands_list).returncode == 0:
    print ("Success: Trim video.")
else:
    print ("Error: Trim video!!!")

# Convert trimmed video to mp3
commands_list2 = convert_mp3(ffmpeg, vfile, ofile, bitrate)
print(commands_list2)
if subprocess.run(commands_list2).returncode == 0:
    print ("Sucess: Convert video to mp3.")
else:
    print ("Error: Convert video to mp3!!!")
