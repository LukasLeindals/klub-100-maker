#!/usr/bin/env python3
import argparse
import os
import subprocess

err = subprocess.Popen(['pip', 'install', 'ffmpeg'], 
                       stdout=subprocess.DEVNULL, 
                       stderr=subprocess.PIPE).communicate()[1]

if len(err) != 0:
    print(err)
    exit(1)

def prepare_shoutout(input, output, t=-14, trim = False, ss = 0, length = 5):
     """
    Prepares a shoutout by normalising, fading and more
    ---------------------------------------------
    input = The input file to prepare
    output = The output file name
    t = the target volume in LUFS (-70 to -5)
    trim = whether or not to trim the shoutout
    ss = the position to start the trim at
    length = the length of the shoutout
    """
    print('Preparing', input + '...')

    # trim
    p1 = subprocess.Popen(['ffmpeg',
                           '-loglevel', 'error',
                           '-ss', str(ss),
                           '-i', input, '-t', str(length), '-f', 'wav', '-'],
                          stdout=subprocess.PIPE)
    
    # two-pass ebu r128 loudnorm filter
    # loudnorm pass 1
    p2 = subprocess.Popen(['ffmpeg', '-loglevel', 'error',
                           '-i', input,
                           '-pass', '1', '-af', 'loudnorm=I=' + str(t) + ':TP=-1',
                           '-f', 'wav', '-y', os.devnull],  # generate log in null
                          stdin=subprocess.PIPE,
                          stdout=subprocess.PIPE)
    
    # loudnorm pass 2
    p3 = subprocess.Popen(['ffmpeg', '-loglevel', 'error',
                           '-i', input,
                           '-pass', '2', '-af', 'loudnorm=I=' + str(t) + ':TP=-1',
                           '-f', 'wav', '-y', output],
                          stdin=subprocess.PIPE,
                          stdout=subprocess.PIPE)
    
    trimmed = p1.communicate()[0]

    p2.communicate(trimmed)
    p3.communicate()

if __name__ == '__main__':
    
    parser = argparse.ArgumentParser()
    parser.add_argument('input', type=str, help='Input file')
    parser.add_argument('output', type=str, help='Output file')
    parser.add_argument('-t', type=int, default=-14, help='Target volume in LUFS (-70 to -5)')
    
    args = parser.parse_args()
    
    prepare_shoutout(args.input, args.output, args.t)
