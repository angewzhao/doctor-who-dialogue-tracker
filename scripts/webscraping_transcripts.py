"""
This webscrapes the transcripts, as they are, from http://www.chakoteya.net/DoctorWho. This script does this for all
of the transcripts available for Doctor Who and includes audiobook text.

"""

import requests, bs4, webbrowser, os, html2text, re, time, random
import numpy as np
from pathlib import Path


# This function downloads the url and returns the html that has been parsed with Beautiful Soup.
def get_html(url):
    res = requests.get(url)
    res.raise_for_status
    return bs4.BeautifulSoup(res.text, 'html.parser')


# This function returns, in a string, the number of the doctor given the url of each doctor's transcript homepage.
def get_doctor_num(url):
    return re.findall('\d+', url)[0]


# This function returns the absolute file path of the folder where the transcrips will be stored.
# ie: C:\Users\angel\GitHub\doctor-who-transcripts\data-raw\doctor_who_transcripts_2\doctor_2 for Doctor 2.
def get_dir_name(dir_root, url):
    folder_name = 'doctor_' + get_doctor_num(url)
    return Path(dir_root, folder_name)


# This function returns the file name of each transcript, which follows the season_episodenum_titleofepisode
def get_file_name(transcript_text, transcript_url, dir_name):
    episode_title = re.findall('[**].+[**]', transcript_text)

    ## Use double quotes to get the punctuation, white space, and numerical title names
    episode_title = re.findall("[A-z0-9, ']+", episode_title[0])[0]
    episode_title = re.sub('\s', '_', episode_title.lower())

    ## The name here refers to the season and episode number, ie 33-4
    name = re.sub('.htm', '', (os.path.basename(transcript_url)))
    name = re.sub('[-]', '_', name)
    file_name = name + "_" + episode_title + ".txt"
    return (Path(dir_name, file_name))


# This function compiles all of the links to the homepages of each doctor's transcipts.
# ie: http://www.chakoteya.net/DoctorWho/episodes11.html for the 11th Doctor.
def get_doctor_transcript_links(home_url):
    doctor_transcript_links = []
    soup_home = get_html(home_url)

    for link in soup_home.find_all('a', href=True):
        # This is to format the 8th's doctor's original link
        doctor_link = re.sub("[.]{2}[/]", "", link['href'])

        if (doctor_link not in doctor_transcript_links) and (re.search("episodes([0-9])+", doctor_link) is not None):
            doctor_transcript_links += [doctor_link]

    # This checks if doctor_transcript_links is empty.
    if not doctor_transcript_links:
        print('There are no transcripts for any of the doctors.')

    return doctor_transcript_links


# This function gets all of the individual transcript links for each episode given a doctor's transcript homepage,
# the transcript homepage, and the href individual links needed to make each episode.
def get_transcript_links(transcript_hrefs, home_url, doctor_url):
    transcript_urls = []
    for href in transcript_hrefs:
        # Ensure that each link taken is unique.
        if href not in transcript_urls:
            link = href.get('href')

        # Select only links that are related to episodes.
        if "index.html" not in link and "../StarTrek/index.html" not in link:
            # Use a special home_url for Doctor 8.
            if get_doctor_num(doctor_url) == "8":
                transcript_url = 'http://www.chakoteya.net/8Doctor/' + link
            else:
                # This creates the entire working link for each episode transcript.
                transcript_url = home_url + link

            transcript_urls += [transcript_url]
    return transcript_urls


# This function downloads the transcripts, given
def download_transcripts(transcripts, dir_root, url):
    # This sets up the html2text handler to ignore links and images in the html.
    h = html2text.HTML2Text()
    h.ignore_links = True
    h.ignore_images = True

    dir_name = get_dir_name(dir_root, url)

    # Getting each individual link for the transcripts
    for transcript_url in transcripts:

        print('Downloading transcript %s...' % (transcript_url))

        transcript_soup = get_html(transcript_url)
        # This encodes the parsed html into utf-8, and then decodes it according to utf-8 to set up the file for the
        # html2text.
        htmltext = transcript_soup.encode('utf-8').decode('utf-8', 'ignore')

        # This turns the parsed html into readable ASCII text with no tags.
        transcript_text = h.handle(htmltext)

        # Download the transcripts. Open file with encoding to ensure all characters read can be encoded.
        transcript_file = open(get_file_name(transcript_text, transcript_url, dir_name), 'w', encoding='utf-8')
        for text_line in transcript_text:
            transcript_file.write(text_line)

        transcript_file.close()

    print("Done.")


# This function webscrapes all of the transcripts for Doctor Who, including various audiobooks, TV episodes, and webcast videos.
# This does not include any of the spin-offs.
def webscrape_all_transcripts(pathlib_dir, os_dir):
    home_url = 'http://www.chakoteya.net/DoctorWho/'

    doctor_transcript_links = get_doctor_transcript_links(home_url)

    for url in doctor_transcript_links:
        if get_doctor_num(url) == "8":
            doctor_url = 'http://www.chakoteya.net/' + url
        else:
            doctor_url = home_url + url

        soup = get_html(doctor_url)

        print('Downloading transcripts for doctor: %s...' % (doctor_url))

        # Select for only the <a> tags that are after a <td> tag.
        transcript_hrefs = soup.select('td a')

        # This checks if transcript_hrefs is empty
        if not transcript_hrefs:
            print('There are no transcripts for doctor ' + get_doctor_num(doctor_url))

        # Ensure that only one of each link has been taken down, and clean up links for only doctor who.
        transcript_urls = get_transcript_links(transcript_hrefs, home_url, doctor_url)

        # Make the doctor_x folder for the transcripts to be stored in
        folder_name = os_dir + 'doctor_' + get_doctor_num(doctor_url)

        os.makedirs(folder_name, exist_ok=True)
        # Download the transcripts
        download_transcripts(transcript_urls, pathlib_dir, doctor_url)

        # Break 3-10 seconds to ensure won't get kicked off server.
        time.sleep(random.randint(3, 10))

    print("Done.")


def main():
    home_pathlib_dir = Path(r'C:\Users\angel\GitHub\doctor-who-dialogue-tracker\data-raw\doctor_who_transcripts')
    home_os_dir = 'C:\\Users\\angel\\GitHub\\doctor-who-dialogue-tracker\\data-raw\\doctor_who_transcripts\\'

    webscrape_all_transcripts(home_pathlib_dir, home_os_dir)

# When executed directly, then condition is true. If executed indirectly, like it's imported, then the if statement
# evaluates to false.
if __name__ == "__main__":
    main()
