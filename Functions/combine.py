#!/usr/bin/env python3
import argparse
import csv
import subprocess
import os

err = subprocess.Popen(['pip', 'install', 'ffmpeg'], 
                       stdout=subprocess.DEVNULL, 
                       stderr=subprocess.PIPE).communicate()[1]

if len(err) != 0:
    print(err)
    exit(1)

# parser = argparse.ArgumentParser()
# parser.add_argument('-shoutouts', type=str, default=os.path.join(os.path.curdir, 'prepared_shoutouts'),
#                     help='Input shoutouts folder')
# parser.add_argument('-tracks', type=str, default=os.path.join(os.path.curdir, 'prepared_tracks'),
#                     help='Input tracks folder')
# parser.add_argument('-output', type=str, default=os.path.join(os.path.curdir, 'klub.mp3'),
#                     help='Output file')

# args = parser.parse_args()

# if not os.path.exists(args.shoutouts) or not os.path.exists(args.tracks):
#     exit(1)

def combine(club_name = "klub.csv", prep_shoutout_path = None, prep_tracks_path = None, output_name = None, fileformat = "mp3", with_shoutouts = True):
    """
    Combines songs and shoutouts
    -----------------------------------
    club_name = the name of the club csv file
    prep_shoutout_path = path for the folder with the prepared shoutouts
    prep_tracks_path = path for the folder with the prepared tracks
    output_name = navnet på den lyd fil der skal laves med klub 100
    fileformat = the fileformat to use for the club
    with_shoutout = whether or not to use shoutouts
    """
    shoutouts = os.path.join(os.path.curdir, 'prepared_shoutouts') if ((prep_shoutout_path is None) & (with_shoutouts)) else prep_shoutout_path
    tracks = os.path.join(os.path.curdir, 'prepared_tracks') if prep_tracks_path is None else prep_tracks_path
    output = os.path.join(os.path.curdir, 'klub.' + fileformat) if output_name is None else os.path.join(os.path.curdir, output_name+ fileformat)
    inputs = []

    with open(club_name, 'rt') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        
        for i, row in enumerate(reader, 1):
            if with_shoutouts:
                inputs.append('-i')
                inputs.append(os.path.join(shoutouts, str(i) + '.wav'))
            
            inputs.append('-i')
            inputs.append(os.path.join(tracks, str(i) + '.wav'))

    n = 2*i if with_shoutouts else i
    filter_ = ''.join(('[' + str(a) + ':0]' for a in range(0, n))) + 'concat=n=' + str(n) + ':v=0:a=1[out]'

    process = subprocess.Popen(['ffmpeg', *inputs, '-filter_complex', filter_, '-map', '[out]', output],
                            stdout=subprocess.PIPE)
    process.communicate()
