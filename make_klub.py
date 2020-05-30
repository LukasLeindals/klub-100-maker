from Functions.dl import download, download_all
from Functions.prepare_track import prepare_all_tracks
from Functions.prepare_shoutout import prepare_all_shoutouts
from Functions.prepare_csv import create_song_csv, create_shoutout_csv, get_trim_vals
from Functions.combine import combine
import os



def make_club(club_folder, club_file, n_songs = 100, output_name = "klub", shoutout_type = "none", song_vol = -14, so_vol = -14, 
                fade = 3, song_length = 60, file_format = "mp3"):
    """
    Makes a club 100
    -------------------------------------------------------------
    club_folder: the folder in which the club xlsx is placed \n
    club_file: either an xlsx file with the "Sange" and "Shoutout" sheets or csv with the songs. Can also pass a list of csv's, where the first element is the name of the csv for the songs and the second is csv with shoutouts \n
    n_songs = the length of the club 100 \n
    shoutout_type: a string defining the type of shoutout, choices are "none", "link" and "own" \n
    song_vol = the song volume in LUFS (-70 to -5) \n
    so_vol = the shoutout volume in LUFS (-70 to -5) \n
    fade = the number of seconds to fade each song \n
    song_length = length of each song \n
    file_format = the file format of the output file
    """
    
    # initialisation
    print("Beginning to make the Club 100...")
    song_csv = club_folder+"/Songs.csv"
    shoutout_csv = club_folder+"/Shoutouts.csv"
    song_folder = club_folder+"/songs"
    shoutout_folder = club_folder + "/shoutouts"
    prep_song_folder = club_folder + "/prepared_songs"
    prep_shoutout_folder = club_folder + "/prepared_shoutouts"

    # prepare songs csv
    filename, file_extension = os.path.splitext(club_file)
    if type(club_file) == list:
        pass
    else:
        create_song_csv(file_name = club_folder+"/"+club_file, csv_name = song_csv, n_songs=n_songs)



    # Download songs
    download_all(dl_path=song_folder, csv_name=song_csv)
    
    # prepare shoutout csv, only necesary if shoutouts is obtained through links
    if shoutout_type == "link":
        create_shoutout_csv(club_folder+"/"+club_file, n_shoutouts=n_songs, shoutout_sheet="Shoutouts", csv_name = shoutout_csv)
        download_all(dl_path = shoutout_folder, csv_name=shoutout_csv)


    # prepare tracks
    prepare_all_tracks(songs_csv=song_csv, input = song_folder, output = prep_song_folder, t = song_vol, f = fade, length = song_length)

    # prepare shoutouts
    with_shoutouts = True if (shoutout_type == "link" or shoutout_type == "own") else False

    if with_shoutouts:
        trim_vals = get_trim_vals(shoutouts_csv=shoutout_csv) if shoutout_type == "link" else None
        prepare_all_shoutouts(songs_csv=song_csv, input = shoutout_folder, output = prep_shoutout_folder, t = so_vol, trim_vals = trim_vals)


    # combine the tracks and shoutouts
    combine(songs_csv= song_csv, prep_shoutout_path = prep_shoutout_folder, prep_tracks_path = prep_song_folder, output_name = club_folder+"/"+output_name, file_format = file_format, with_shoutouts = with_shoutouts)

if __name__ == "__main__":
    # club_folder = "Examples/Børne Klub 100/"
    # club = club_folder+"test_kid2.xlsx"
    n = 3
    make_club(club_folder = "Examples/Børne Klub 100", club_file = "test_kid2.xlsx", n_songs = 3, shoutout_type="link", output_name = "test", file_format = "mp3")



    # make_club(club_folder, club, n_songs = n, output_name = "test_KID2", shoutout_type = "link")
    # combine(songs_csv= club_folder+"Songs.csv", prep_shoutout_path = None, prep_tracks_path = None, output_name = "test_KID2", fileformat = "mp3", with_shoutouts = True)

   
    

    

    
