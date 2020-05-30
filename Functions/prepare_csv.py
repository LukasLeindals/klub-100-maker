import pandas as pd
import os



def create_song_csv(file_name, n_songs = 100, song_sheet = "Sange", csv_name = "Songs.csv"):
    """
    Creates a csv in the right format to use for the make_klub function. File must either be xlsx or csv and have the headers "Sang - Kunstner", "link", "starttidspunkt (i sek)", "Shoutout"
    -------------------------------------------
    file_name = file to make the songs csv from \n
    n_songs = how many songs to use (fill be taken from start of the file) \n
    song_sheet = if the file is an .xslx file, the name of the sheet containing the songs must be given here \n
    csv_name = name of the output csv, must have the .csv extension
    """


    # determine file extension
    filename, file_extension = os.path.splitext(file_name)

    # make sure extension is supported
    supported_extensions = [".xlsx", ".csv"]
    assert (file_extension in supported_extensions)

    # create the csv 
    if file_extension == ".xlsx":
        songs = pd.read_excel(file_name, sheet_name=song_sheet, usecols = ["Sang - Kunstner", "link", "starttidspunkt (i sek)", "Shoutout"])
    elif file_extension == ".csv":
        songs = pd.read_csv(file_name, usecols = ["Sang - Kunstner", "link", "starttidspunkt (i sek)", "Shoutout"])

    songs.iloc[:n_songs, :].to_csv(csv_name, index = False, header = False)


def create_shoutout_csv(file_name, n_shoutouts = 100, shoutout_sheet = "Shoutouts", csv_name = "Shoutouts.csv", max_length = 45):
    """
    Creates a csv in the right format to use for the make_klub function. File must either be xlsx or csv and have the headers "Shoutout titel", "link", "starttidspunkt (i sek)", "sluttidspunkt (i sek)"
    -------------------------------------------
    file_name = file to make the shoutout csv from \n
    n_shoutouts = how many shoutouts to use (fill be taken from start of the file). This should match the number of songs used \n
    shoutout_sheet = if the file is an .xslx file, the name of the sheet containing the shoutputs must be given here \n
    csv_name = name of the output csv, must have the .csv extension \n
    max_length = the maximum length of a shoutout, if the no end time of the shoutout is given, this shoutout will be trimmed to this length
    """
    
    # determine file extension
    filename, file_extension = os.path.splitext(file_name)

    # make sure file is the right extension
    supported_extensions = [".xlsx", ".csv"]
    assert (file_extension in supported_extensions)

    # create the csv
    if file_extension == ".xlsx":
        shoutouts = pd.read_excel(file_name, sheet_name = shoutout_sheet, usecols = ["Shoutout titel", "link", "starttidspunkt (i sek)", "sluttidspunkt (i sek)"])
    elif file_extension == ".csv":
        shoutouts = pd.read_csv(file_name, usecols = ["Shoutout titel", "link", "starttidspunkt (i sek)", "sluttidspunkt (i sek)"])
    shoutouts["SO length"] = shoutouts["sluttidspunkt (i sek)"]-shoutouts["starttidspunkt (i sek)"]
    shoutouts["SO length"] = shoutouts["SO length"].fillna(max_length)
    shoutouts.iloc[:n_shoutouts, [0, 1, 2, 4]].to_csv(csv_name, index = False, header = False)

def get_trim_vals(shoutouts_csv = "Shoutouts.csv"):
    """
    Gets the values to use for trimming the shoutouts, returns a data frame with the starts times in the first column and the the length as the second.
    ------------------------------------------
    shoutouts_csv = name of the csv with the shoutouts
    """
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