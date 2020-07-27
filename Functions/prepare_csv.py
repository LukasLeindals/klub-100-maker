import pandas as pd
import os
import numpy as np
import shutil



def create_song_csv(file_name, n_songs = 100, song_sheet = "Sange", csv_name = "Songs.csv", diff_song_length = False):
    """
    Creates a csv in the right format to use for the make_klub function. File must either be xlsx or csv and have the headers "Sang - Kunstner", "link", "starttidspunkt (i sek)", "Shoutout"
    -------------------------------------------
    file_name = file to make the songs csv from \n
    n_songs = how many songs to use (fill be taken from start of the file) \n
    song_sheet = if the file is an .xslx file, the name of the sheet containing the songs must be given here \n
    csv_name = name of the output csv, must have the .csv extension \n
    diff_song_length = whether the songs have varying/different lengths \n
    """
    print("Creating the song csv...")

    # determine file extension
    filename, file_extension = os.path.splitext(file_name)

    # make sure extension is supported
    supported_extensions = [".xlsx", ".csv"]
    if not (file_extension in supported_extensions):
        raise AssertionError("Please use a valid file extension (xlsx or csv)")

    # create the csv 
    cols = ["Sang - Kunstner", "link", "starttidspunkt (i sek)", "sluttidspunkt (i sek)", "Shoutout", "behold placering"] if diff_song_length else ["Sang - Kunstner", "link", "starttidspunkt (i sek)", "Shoutout", "behold placering"]

    if file_extension == ".xlsx":
        songs = pd.read_excel(file_name, sheet_name=song_sheet, usecols = cols).dropna(how = "all")
    elif file_extension == ".csv":
        songs = pd.read_csv(file_name, usecols = cols)

    if diff_song_length:
        songs["Song length"] = songs["sluttidspunkt (i sek)"]-songs["starttidspunkt (i sek)"]
        songs["Song length"] = songs["Song length"].fillna(60)
        songs = songs.loc[:, ["Sang - Kunstner", "link", "starttidspunkt (i sek)", "Song length", "Shoutout"]]

    songs.iloc[:n_songs, :].to_csv(csv_name, index = False, header = False)


def create_shoutout_csv(file_name, n_shoutouts = 100, shoutout_sheet = "Shoutouts", csv_name = "Shoutouts.csv", max_length = 45):
    """
    Creates a csv in the right format to use for the make_klub function. File must either be xlsx or csv and have the headers "Shoutout titel", "link", "starttidspunkt (i sek)", "sluttidspunkt (i sek)"
    -------------------------------------------
    file_name = file to make the shoutout csv from \n
    n_shoutouts = how many shoutouts to use (will be taken from start of the file). This should match the number of songs used \n
    shoutout_sheet = if the file is an .xslx file, the name of the sheet containing the shoutputs must be given here \n
    csv_name = name of the output csv, must have the .csv extension \n
    max_length = the maximum length of a shoutout, if the no end time of the shoutout is given, this shoutout will be trimmed to this length
    """

    print("Creating the shoutout csv...")
    
    # determine file extension
    filename, file_extension = os.path.splitext(file_name)

    # make sure file is the right extension
    supported_extensions = [".xlsx", ".csv"]
    assert (file_extension in supported_extensions)

    # create the csv
    if file_extension == ".xlsx":
        shoutouts = pd.read_excel(file_name, sheet_name = shoutout_sheet, usecols = ["Shoutout titel", "link", "starttidspunkt (i sek)", "sluttidspunkt (i sek)"]).dropna(how = "all")
    elif file_extension == ".csv":
        shoutouts = pd.read_csv(file_name, usecols = ["Shoutout titel", "link", "starttidspunkt (i sek)", "sluttidspunkt (i sek)"])
    shoutouts["SO length"] = shoutouts["sluttidspunkt (i sek)"]-shoutouts["starttidspunkt (i sek)"]
    shoutouts["SO length"] = shoutouts["SO length"].fillna(max_length)
    shoutouts.iloc[:n_shoutouts, [0, 1, 2, 4]].to_csv(csv_name, index = False, header = False)

def get_trim_vals(csv = "Shoutouts.csv"):
    """
    Gets the values to use for trimming the shoutouts, returns a data frame with the starts times in the first column and the the length as the second.
    ------------------------------------------
    csv = name of the csv to extract trim values from \n
    """
    lens = pd.read_csv(csv, header = None)
    print(lens)
    lens = lens.select_dtypes(include=[np.number])
    lens.columns = list(range(2))
    return lens

def mix_song_pos(song_csv = "Songs.csv", diff_song_length = False):
    """
    Mixes up the order of the songs or shoutouts
    ---------------------------------------
    csv: a csv in the format of create_song_csv/shoutout_csv, where a character in the column "behold placering", keeps the song in its original position \n
    diff_song_length: whether the song_csv contains the column "sluttidspunkt (i sek)" or not
    """
    df = pd.read_csv(song_csv, usecols = [5]) if diff_song_length else pd.read_csv(song_csv, usecols = [4], header = None, squeeze = True)
    l = len(df)
    mix_loc = list(*np.where(pd.isnull(df)))
    keep_loc = [i for i in range(l) if i not in mix_loc]
    order = []
    perm_mix = np.random.permutation(mix_loc)
    for i in range(l):
        if i in keep_loc:
            order.append(i)
        else:
            order.append(perm_mix[0])
            perm_mix = np.delete(perm_mix, 0)
    
    pd.read_csv(song_csv, header = None).reindex(order).to_csv(song_csv, index = False, header = False)


def arrange_shoutout_csv(song_csv = "Songs.csv", shoutout_csv = "Shoutouts.csv", diff_song_length = False):
    """
    Arranges the shoutout csv due to the placement in the song csv
    """
    song_so = pd.read_csv(song_csv, usecols = [4]) if diff_song_length else pd.read_csv(song_csv, usecols = [3], header = None, squeeze = True).values
    shoutout_so = pd.read_csv(shoutout_csv, usecols = [0], header = None, squeeze = True).values

    missing_so = [t for t in song_so if (t is not np.nan) & (t not in shoutout_so)]
    if len(missing_so) is not 0:
        print(f"These shoutouts does not exist in the shoutout csv/sheet: {missing_so}! Please insert the same name in the song sheet as given in the shoutout sheet if the shoutout should follow a specific song.")

    order = []
    perm_mix = np.random.permutation([i for i in range(len(song_so)) if shoutout_so[i] not in song_so])

    for i in range(len(song_so)):
        if song_so[i] in shoutout_so:
            order.append(*list(*np.where(shoutout_so == song_so[i])))
        else:
            order.append(perm_mix[0])
            perm_mix = np.delete(perm_mix, 0)

    pd.read_csv(shoutout_csv, header = None).reindex(order).to_csv(shoutout_csv, index = False, header = False)

def rename_sound(infile, outfile):
    import subprocess
    err = subprocess.Popen(['pip', 'install', 'ffmpeg'], 
                       stdout=subprocess.DEVNULL, 
                       stderr=subprocess.PIPE).communicate()[1]

    p1 = subprocess.Popen(['ffmpeg',
                           '-loglevel', 'error',
                           '-i', infile, '-f', 'm4a', '-'],
                          stdout=subprocess.PIPE)
    p2 = subprocess.Popen(['ffmpeg',
                           '-loglevel', 'error',
                           '-f', 'wav', '-y', outfile],
                          stdin=subprocess.PIPE,
                          stdout=subprocess.PIPE)
    
    p = p1.communicate()[0]
    
    return p2.communicate(p1)[0]

def name_own_shoutouts(song_csv = "Songs.csv", org_shoutout_folder = "shoutouts", new_shoutout_folder = "shoutouts_numbered", diff_song_length = False):
    """
    Renames all the recorded shoutouts to give them the correct order
    """
    song_so = pd.read_csv(song_csv, usecols = [4]) if diff_song_length else pd.read_csv(song_csv, usecols = [3], header = None, squeeze = True).values
    
    if not os.path.exists(new_shoutout_folder):
        os.mkdir(new_shoutout_folder)
    
    files = [os.path.splitext(f)[0] for f in os.listdir(org_shoutout_folder)]

    missing_so = [t for t in song_so if (t is not np.nan) & (t not in files)]
    if len(missing_so) is not 0:
        print(f"These shoutouts does not exist in the shoutout folder: {missing_so}! Please insert the same name in the song sheet as given in the shoutout folder if the shoutout should follow a specific song.")

    
    perm_mix = np.random.permutation([i for i in range(len(song_so)) if song_so[i] not in files])
    order = {}
    song_so_num = [i for i, f in enumerate(song_so) if f is not np.nan]

    for i in range(len(files)):
        if files[i] in song_so:
            order[files[i]] = song_so_num[0]+1
            song_so_num = np.delete(song_so_num, 0)
        else:
            print(perm_mix)
            order[files[i]] = perm_mix[0]+1
            perm_mix = np.delete(perm_mix, 0)
    
    
    with multiprocessing.Pool() as p:
        for i, f  in enumerate(os.listdir(org_shoutout_folder)):
            filename, file_extension = os.path.splitext(f)
            infile = os.path.join(input, str(i) + '.wav')
            outfile = os.path.join(output, str(i) + '.wav')
            
            if not os.path.exists(f):
                continue
            
            if isinstance(length, pd.DataFrame):
                p.apply_async(prepare_track, (infile, outfile, length.iloc[i-1,0], t, f, length.iloc[i-1,1]))
            else:
                p.apply_async(prepare_track, (infile, outfile, row[2], t, f, length))


if __name__ == "__main__":
    # create_song_csv("Examples/Børne Klub 100/Børne Klub 100.xlsx", csv_name="Songs.csv", diff_song_length=False, n_songs=14)
    # create_shoutout_csv("Examples/Børne Klub 100/Børne Klub 100.xlsx", csv_name="Shoutouts.csv", n_shoutouts=14) 
    # # print(get_trim_vals("test_songs.csv"))
    # mix_song_pos("Songs.csv", diff_song_length = False)
    # arrange_shoutout_csv(song_csv = "Songs.csv", shoutout_csv="Shoutouts.csv")
    # # arrange_shoutout_csv(song_csv = "test_songs2.csv", shoutout_csv="test_so2.csv")


    # create_song_csv("test/template.xlsx", n_songs = 8, csv_name="test/Songs.csv")
    # mix_song_pos(song_csv="test/Songs.csv")
    # name_own_shoutouts(song_csv = "test/Songs.csv", org_shoutout_folder = "test/shoutouts", new_shoutout_folder = "test/shoutouts_numbered")
    rename_sound("test/shoutouts/Badeland.m4a", "test/shoutouts_numbered/1.wav")