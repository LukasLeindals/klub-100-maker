from Functions.prepare_csv import create_song_csv
from Functions.dl import download_all

if __name__ == "__main__":
    # create_song_csv(file_name="Børne Klub 100 - Sange.csv",n_songs=3)
    # create_song_csv(file_name="Examples/Børne Klub 100/test_kid2.xlsx", n_songs=3,csv_name = "test1.csv")

    download_all(dl_path = "Examples/test_dl", csv_name = "Songs.csv")