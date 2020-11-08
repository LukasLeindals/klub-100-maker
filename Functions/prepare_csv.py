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
    --------------------------------------------------------------
    song_csv: name of the csv containing the song titles \n
    shoutout_csv: name of the csv containing the shoutout names and links \n
    diff_song_length: true or false whether the songs should have varying lengths
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
    """
    Changes name and fileformat of sound file
    -------------------------------------------
    infile: the input file \n
    outfile: the output file
    """
    import subprocess
    err = subprocess.Popen(['pip', 'install', 'ffmpeg'], 
                       stdout=subprocess.DEVNULL, 
                       stderr=subprocess.PIPE).communicate()[1]

    if len(err) != 0:
        print(err)
        exit(1)

    return subprocess.Popen(['ffmpeg', '-i', infile, outfile]).communicate()

def name_own_shoutouts(song_csv = "Songs.csv", org_shoutout_folder = "shoutouts", new_shoutout_folder = "shoutouts_numbered", diff_song_length = False, conversion_csv = "shoutout_to_number.csv"):
    """
    Renames all the recorded shoutouts to give them the correct order
    ------------------------------------------------------------------
    song_csv: name of the csv with the song titles and links \n
    org_shoutout_folder: name of the folder with the shoutouts to be renamed \n
    new_shoutout_folder: name of the folder to place the renamed shoutouts in \n
    diff_song_length: whether the songs have varying length (bool) \n
    conversion_csv: name to give the csv with an overview of the original shoutout names and the numbered names
    """
    import multiprocessing

    if not os.path.exists(new_shoutout_folder):
        os.mkdir(new_shoutout_folder)
    else:
        overwrite = input(f"The new_shout_folder: {new_shoutout_folder} already exists, would you like to overwrite this? [y/n] \n").lower()
        while overwrite not in ["y", "n"]:
            overwrite = input(f"The new_shout_folder: {new_shoutout_folder} already exists, would you like to overwrite this? [y/n] \n").lower()
        
        if overwrite is "n":
            org_len = len(os.listdir(org_shoutout_folder))
            new_len = len(os.listdir(new_shoutout_folder))

            if org_len is not new_len:
                raise ValueError(f"The number of orignal shoutouts ({org_len}) does not match the number of new shoutouts ({new_len}), please make sure all shoutouts have been numbered, by e.g. chossing to overwrite the existing folder for the new shoutouts.")
        
        else:
            shutil.rmtree(new_shoutout_folder)
            os.mkdir(new_shoutout_folder)

    song_so = pd.read_csv(song_csv, usecols = [4]) if diff_song_length else pd.read_csv(song_csv, usecols = [3], header = None, squeeze = True).values
    sos = [os.path.splitext(f)[0] for f in os.listdir(org_shoutout_folder)]
    form = [os.path.splitext(f)[1] for f in os.listdir(org_shoutout_folder)]
    # print(song_so)
    # wav_names = [i+1 for i in range(len(sos))]

    missing_so = [t for t in song_so if (t is not np.nan) & (t not in sos)]
    if len(missing_so) is not 0:
        raise ValueError(f"These shoutouts does not exist in the shoutout folder: {missing_so}! Please insert the same name in the song sheet as given in the shoutout folder if the shoutout should follow a specific song.")


    perm_mix = np.random.permutation([i for i in range(len(song_so)) if song_so[i] not in sos])
    # print(perm_mix)
    order = {}
    # song_so_num = [i for i, f in enumerate(song_so) if f is not np.nan]

    files = os.listdir(org_shoutout_folder)
    # fiks at den bruger placeringen i csv i stedet for bare at tage dem i den rækkefølge de ligger i mappen
    for i in range(len(files)):
        if song_so[i] is not np.nan:
            order[song_so[i]+form[i]] = str(i+1)+".wav"
            # song_so_num = np.delete(song_so_num, 0)
        else:
            order[files[perm_mix[0]]] = str(i+1)+".wav"
            perm_mix = np.delete(perm_mix, 0)


    with multiprocessing.Pool() as p:
        for key, value in order.items():
            infile = org_shoutout_folder+"/"+key
            outfile = new_shoutout_folder+"/"+value

            print(infile, "------>", outfile)

            p.apply_async(rename_sound, (infile, outfile))

        p.close()
        p.join()


    pd.DataFrame.from_dict(order, orient = "index").to_csv(conversion_csv, index = True, header = False)

    print(f"The own shoutouts have now been renamed to fit the club 100 format and can be found in {new_shoutout_folder}. Furthermore, a csv showing the new naming can be found as {conversion_csv}")
    


if __name__ == "__main__":
    # create_song_csv("Examples/Bad Bitch/klub100.xlsx", csv_name="Songs.csv", diff_song_length=False, n_songs=100)
    # create_shoutout_csv("Examples/Børne Klub 100/Børne Klub 100.xlsx", csv_name="Shoutouts.csv", n_shoutouts=14) 
    # # print(get_trim_vals("test_songs.csv"))
    # mix_song_pos("Songs.csv", diff_song_length = False)
    # arrange_shoutout_csv(song_csv = "Songs.csv", shoutout_csv="Shoutouts.csv")
    # # arrange_shoutout_csv(song_csv = "test_songs2.csv", shoutout_csv="test_so2.csv")


    # create_song_csv("test/template.xlsx", n_songs = 8, csv_name="test/Songs.csv")
    # mix_song_pos(song_csv="test/Songs.csv")
    name_own_shoutouts(song_csv = "Examples/Bad Bitch/Songs.csv", org_shoutout_folder = "Examples/Bad Bitch/shoutouts", new_shoutout_folder = "Examples/Bad Bitch/shoutouts_numbered", conversion_csv="Examples/Bad Bitch/so_to_num.csv")
    # rename_sound("test/shoutouts/bada bing.m4a", "test/shoutouts_numbered/3.wav")