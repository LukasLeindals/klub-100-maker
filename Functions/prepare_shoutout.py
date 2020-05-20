#!/usr/bin/env python3
import argparse
import os
import subprocess
import csv
import multiprocessing

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
        
        # normalize
        # two-pass ebu r128 loudnorm filter
        # loudnorm pass 1
        p2 = subprocess.Popen(['ffmpeg',
                            '-loglevel', 'error',
                            '-i', '-',
                            '-pass', '1', '-af', 'loudnorm=I=' + str(t) + ':TP=-1',
                            '-f', 'wav', '-y', os.devnull],  # generate log but no other output
                            stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE)
        
        # loudnorm pass 2
        p3 = subprocess.Popen(['ffmpeg',
                            '-loglevel', 'error',
                            '-i', '-',
                            '-pass', '2', '-af', 'loudnorm=I=' + str(t) + ':TP=-1',
                            '-f', 'wav', '-'
                            ],
                            stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE)
        
        # fade
        f=0
        p4 = subprocess.Popen(['ffmpeg',
                            '-loglevel', 'error',
                            '-i', '-', '-af',
                            'afade=t=in:ss=0:d=' + str(f) +
                            ',afade=t=out:st=' + str(ss+length) + ':d=' + str(f),
                            '-f', 'wav', '-y', output],
                            stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE)

    else:
        # two-pass ebu r128 loudnorm filter
        # loudnorm pass 1
        p1 = subprocess.Popen(['ffmpeg', '-loglevel', 'error',
                            '-i', input,
                            '-pass', '1', '-af', 'loudnorm=I=' + str(t) + ':TP=-1',
                            '-f', 'wav', '-y', os.devnull],  # generate log in null
                            stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE)
        
        # loudnorm pass 2
        p2 = subprocess.Popen(['ffmpeg', '-loglevel', 'error',
                            '-i', input,
                            '-pass', '2', '-af', 'loudnorm=I=' + str(t) + ':TP=-1',
                            '-f', 'wav', '-y', output],
                            stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE)

    if trim:
        trimmed = p1.communicate()[0]
        p2.communicate(trimmed)
        normalized = p3.communicate(trimmed)[0]
        p4.communicate(normalized)[0]

    else:
        p1.communicate()
        p2.communicate()

def prepare_all_shoutouts(songs_csv = "klub.csv", input = None, output = None, t = -14, trim_vals = None): 
    """
    Prepares all shoutouts
    -------------------------
    n_shoutouts = the number of shoutouts in the club 100
    input = input folder with shoutouts
    output = name of output folder
    t = Target volume in LUFS (-70 to -5)
    trim_vals = data frame with start time of SO as first column and length as second
    """

    input = os.path.join(os.path.curdir, 'shoutouts') if input is None else input
    output = os.path.join(os.path.curdir, 'prepared_shoutouts') if output is None else output
    
    if not os.path.exists(input):
        exit(1)
    
    if not os.path.exists(output):
        os.mkdir(output)

    trim = False if trim_vals is None else True
    with multiprocessing.Pool() as p:
        with open(songs_csv, 'rt') as csvfile:
            reader = csv.reader(csvfile, delimiter=',', quotechar='"')
            
            for i, row in enumerate(reader, 1):
                
                infile = os.path.join(input, str(i) + '.wav')
                outfile = os.path.join(output, str(i) + '.wav')
                
                if not os.path.exists(infile):
                    continue
                
                p.apply_async(prepare_shoutout, (infile, outfile, t, trim, trim_vals.iloc[i-1,0], trim_vals.iloc[i-1,1]))
        
        p.close()
        p.join()

