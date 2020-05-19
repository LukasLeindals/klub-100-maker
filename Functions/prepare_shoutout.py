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
    Prepares a shoutout by normalising and more
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
    if trim:
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
    
    if trim:
        trimmed = p1.communicate()[0]
        p2.communicate(trimmed)
    else:
        p2.communicate()
    p3.communicate()

def prepare_all_shoutouts(n_shoutouts = 100, input = None, output = None, t = -14, trim_lengths = None): 
    """
    Prepares all shoutouts
    -------------------------
    csv_name = name of csv with info about club 100 songs
    input = input folder with shoutouts
    output = name of output folder
    t = Target volume in LUFS (-70 to -5)
    """

    input = os.path.join(os.path.curdir, 'shoutouts') if input is None else input
    output = os.path.join(os.path.curdir, 'prepared_shoutouts') if output is None else output
    
    if not os.path.exists(input):
        exit(1)
    
    if not os.path.exists(output):
        os.mkdir(output)

    trim = False if trim_lengths is None else True
    
    with multiprocessing.Pool() as p:
        
            
            
        for i in range(n_shoutouts):
            
            infile = os.path.join(input, str(i) + '.wav')
            outfile = os.path.join(output, str(i) + '.wav')
            
            if not os.path.exists(infile):
                continue
            
            p.apply_async(prepare_shoutout, (infile, outfile, t))
        
        p.close()
        p.join()
