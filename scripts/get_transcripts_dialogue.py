import os, re
from pathlib import Path
import numpy as np
import pandas as pd


# Label the different dialogue lines by who is speaking
def get_names(df):
    text_name = []

    # The numbers in the names are to account for the appearances of other doctors. However, the DOCTOR: will always be
    # the current incarnation
    for line in df['text']:
        name = re.findall('[A-Z0-9 ]+', line)
        extra = re.findall('[(]+|[)]+.|[<]+.|[*]+.|[-]+.', line)

        # This filters for scene changes, comments made at end of the transcript, etc. Anything that isn't dialogue.
        if len(extra) >= 1:
            name = "EXTRANEOUS"
        elif len(name) > 0 and len(name[0]) > 1:
            name = name[0]
        else:
            name = np.NaN
        text_name += [name]

    return text_name


# Turns dialogue into format needed for making word probablity maps.
def clean_dialogue(df):
    text_lines = []

    for line in df['text']:
        if 'DOCTOR:' in line:
            line = line.replace('DOCTOR: ', '')

        line = re.sub("([.]+)|([?]+)|([,]+)|([!]+)", "", line.lower())
        line = re.sub("(\s)+", ", ", line)
        line = re.sub("\n", "", line)

        text_lines += [line]

    return text_lines


def download_dialogue(df, transcript_file_name, all_dialogue_file):
    dialogue_file = open(transcript_file_name, 'w', encoding='utf-8')

    for line in df['text']:
        dialogue_file.write(line)
        all_dialogue_file.write(line)

    dialogue_file.close()


def get_transcript_dialogue(transcript, abs_dialogue_path, all_dialogue_file):
    df = pd.read_table(transcript, header=None, sep="\n")
    df.columns = ['text']

    df['name'] = get_names(df)
    df['name'] = df['name'].ffill()
    df = df.dropna()
    df = df[df['name'] == "DOCTOR"]

    # Removes the "DOCTOR: " in front of the relevant lines.
    df['text'] = clean_dialogue(df)

    download_dialogue(df, abs_dialogue_path, all_dialogue_file)

    print("Done")


def main():
    #transcript_root = 'C:\\Users\\angel\\Desktop\\doctor_who\\data\\doctor_who_transcripts'
    #dialogue_root = 'C:\\Users\\angel\\Desktop\\doctor_who\\data\\doctor_who_dialogue'

    transcript_root = 'C:\\Users\\angel\\GitHub\\doctor-who-transcripts\\data-raw\\doctor_who_transcripts'
    dialogue_root = 'C:\\Users\\angel\\GitHub\\doctor-who-transcripts\\data\\doctor_who_dialogue'

    for folder in os.listdir(transcript_root):
        abs_dialogue_folder = dialogue_root + "\\" + folder
        os.makedirs(abs_dialogue_folder, exist_ok=True)

        abs_transcript_folder = transcript_root + "\\" + folder

        all_dialogue_path = abs_dialogue_folder + "\\" + folder + "_dialogue.txt"

        all_dialogue_file = open(all_dialogue_path, 'w', encoding='utf-8')

        for transcript in os.listdir(abs_transcript_folder):
            abs_transcript_path = abs_transcript_folder + "\\" + transcript

            abs_dialogue_path = abs_dialogue_folder + "\\" + Path(transcript).stem + "_dialogue.txt"
            print(abs_dialogue_path)

            get_transcript_dialogue(abs_transcript_path, abs_dialogue_path, all_dialogue_file)

        all_dialogue_file.close()


# When executed directly, then condition is true. If executed indirectly, like it's imported, then the if statement
# evaluates to false.
if __name__ == "__main__":
    main()
