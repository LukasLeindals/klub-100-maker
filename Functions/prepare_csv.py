import pandas as pd


def create_song_csv(xlsx_name, song_sheet = "Sange", csv_name = "Songs.csv"):
    songs = pd.read_excel(xlsx_name, sheet_name=song_sheet, usecols = ["Sang - Kunstner", "link", "starttidspunkt (i sek)", "Shoutout"])
    songs.to_csv(csv_name)

    return songs

# def create_shoutout_csv(xlsx_name, shoutout_sheet = "Shoutouts"):
#     shoutouts = pd.read_excel(xlsx_name, sheet_name = shoutout_sheet)


# print(create_song_csv("Examples/Børne Klub 100/Børne Klub 100.xlsx"))

# s = pd.read_excel("Examples/Børne Klub 100/Børne Klub 100.xlsx", sheet_name="Sange", usecols = ["link", "sh"])
# print(s.columns)