from Functions.dl import download_all
from Functions.prepare_all_tracks import prepare_all_tracks
from Functions.combine import combine

download_all(dl_path = None, csv_name = "Songs2.csv")
prepare_all_tracks(club_name = "Songs2.csv", input = None, output = None, t = -14, f = 3, length = 60)
combine(club_name = "klub.csv", prep_shoutout_path = None, prep_tracks_path = None, output_name = None, fileformat = "mp3", with_shoutouts = False)