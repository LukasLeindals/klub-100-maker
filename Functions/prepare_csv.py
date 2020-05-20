import pandas as pd




def create_song_csv(xlsx_name, n_songs = 100, song_sheet = "Sange", csv_name = "Songs.csv"):
    """
    Creates a csv in the right format to use for 
    """
    songs = pd.read_excel(xlsx_name, sheet_name=song_sheet, usecols = ["Sang - Kunstner", "link", "starttidspunkt (i sek)", "Shoutout"])
    songs.iloc[:n_songs, :].to_csv(csv_name, index = False, header = False)


def create_shoutout_csv(xlsx_name, n_shoutouts = 100, shoutout_sheet = "Shoutouts", csv_name = "Shoutouts.csv", max_length = 45):
    shoutouts = pd.read_excel(xlsx_name, sheet_name = shoutout_sheet, usecols = ["Shoutout titel", "link", "starttidspunkt (i sek)", "sluttidspunkt (i sek)"])
    shoutouts["SO length"] = shoutouts["sluttidspunkt (i sek)"]-shoutouts["starttidspunkt (i sek)"]
    shoutouts["SO length"] = shoutouts["SO length"].fillna(max_length)
    shoutouts.iloc[:n_shoutouts, [0, 1, 2, 4]].to_csv(csv_name, index = False, header = False)

def get_club_len(xlsx_name, song_sheet_name = "Sange"):
        songs = pd.read_excel(xlsx_name, song_sheet_name)
        songs = songs.iloc[:, 0].dropna()
        return songs.shape[0]

def get_trim_vals(shoutouts_csv = "Shoutouts.csv"):
    lens = pd.read_csv(shoutouts_csv, usecols=[2,3], header = None)
    lens.columns = list(range(2))
    return lens


if __name__ == "__main__":
    # print(create_song_csv("Examples/Børne Klub 100/Børne Klub 100.xlsx"))

    # s = pd.read_excel("Examples/Børne Klub 100/Børne Klub 100.xlsx", sheet_name="Sange", usecols = ["link", "sh"])
    # print(s.columns)


    # create_shoutout_csv("Examples/Børne Klub 100/Børne Klub 100.xlsx", n_shoutouts=5, csv_name="SO.csv")
    # create_song_csv("Examples/Børne Klub 100/Børne Klub 100.xlsx")
    # print(get_club_len("Examples/Børne Klub 100/Børne Klub 100.xlsx"))
    print(get_trim_vals("SO.csv"))