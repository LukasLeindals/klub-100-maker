from Functions.dl import download, download_all
from Functions.prepare_track import prepare_all_tracks
from Functions.prepare_shoutout import prepare_all_shoutouts
from Functions.prepare_csv import create_song_csv, create_shoutout_csv, get_trim_vals
from Functions.combine import combine



if __name__ == "__main__":
    club_folder = "Examples/Børne Klub 100/"
    club = club_folder+"Børne Klub 100.xlsx"
    n = 5

    # create_song_csv(club, csv_name = club_folder+"Songs.csv", n_songs=n)
    # create_shoutout_csv(club, n_shoutouts=n, shoutout_sheet="Shoutouts", csv_name = club_folder+"Shoutouts.csv")

    # download_all(csv_name=club_folder+"Songs.csv", sound_type="tracks")
    # download_all(csv_name=club_folder+"Shoutouts.csv", sound_type="shoutouts")

    # prepare_all_tracks(songs_csv=club_folder+"Songs.csv", input = None, output = None, t = -14, f = 3, length = 60)
    # trim_vals = get_trim_vals(shoutouts_csv=club_folder+"Shoutouts.csv")
    # prepare_all_shoutouts(songs_csv=club_folder+"Songs.csv", input = None, output = None, t = -14, trim_vals = trim_vals)

    combine(songs_csv= club_folder+"Songs.csv", prep_shoutout_path = None, prep_tracks_path = None, output_name = None, fileformat = "mp3", with_shoutouts = True)
