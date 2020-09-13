import requests, bs4, webbrowser, pyperclip, os, html2text, re
from pathlib import Path


def get_doctor_num(url):
    return re.findall('\d+', url)[0]


def get_file_name(transcript_text, transcript_url, dir_name):
    episode_title = re.findall('[**].+[**]', transcript_text)

    ## Use double quotes to get the apostrophe included in the regex.
    episode_title = re.findall("[A-z0-9, ']+", episode_title[0])[0]
    episode_title = re.sub('\s', '_', episode_title.lower())

    name = re.sub('.htm', '', (os.path.basename(transcript_url)))
    name = re.sub('[-]', '_', name)
    file_name = name + "_" + episode_title + ".txt"
    return (Path(dir_name, file_name))

def main():
    dir_name = Path(r'C:\Users\angel\GitHub\doctor-who-dialogue-tracker\data-raw\doctor_who_transcripts\doctor_10')

    url = 'http://www.chakoteya.net/DoctorWho/episodes10.html'
    res = requests.get(url)
    res.raise_for_status
    soup = bs4.BeautifulSoup(res.text, 'html.parser')
    transcripts_orig = soup.select('td a')

    transcripts = []
    for href in transcripts_orig:
        if (href not in transcripts):
            link = href.get('href')

        if "index.html" not in link and "../StarTrek/index.html" not in link:
            transcripts += [href]

    if transcripts == []:
        print('There are no transcripts for this doctor.')

    h = html2text.HTML2Text()
    h.ignore_links = True
    h.ignore_images = True

    # Getting each individual link for the transcripts
    for line in transcripts:
        if get_doctor_num(url) == str(8):
            transcript_url = 'http://www.chakoteya.net/8Doctor/' + line.get('href')
        else:
            transcript_url = 'http://www.chakoteya.net/DoctorWho/' + line.get('href')

        print('Downloading transcript %s...' % (transcript_url))
        transcript_res = requests.get(transcript_url)
        transcript_res.raise_for_status

        transcript_soup = bs4.BeautifulSoup(transcript_res.text, 'html.parser')
        htmltext = transcript_soup.encode('utf-8').decode('utf-8', 'ignore')
        transcript_text = h.handle(htmltext)

        # Download the transcripts. Open file with encoding to ensure all characters read can be encoded.
        transcript_file = open(get_file_name(transcript_text, transcript_url, dir_name), 'w', encoding='utf-8')
        for text_line in transcript_text:
            transcript_file.write(text_line)

        transcript_file.close()

    print("Done.")

def main():
    # Remember to change url and dir name each time for each different doctor.
    main()

# When executed directly, then condition is true. If executed indirectly, like it's imported, then the if statement
# evaluates to false.
if __name__ == "__main__":
    main()