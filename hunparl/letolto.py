"""
#TODO
"""
# pylint: disable-msg=too-many-locals

from urllib import parse
from pathlib import Path

import http.client
import requests

from bs4 import BeautifulSoup

def scraper(homedir: str, szam: int = -1)->str:
    """
    szam: kiadvány száma pozitív integer
    ha szam = -1, akkor a legutoljára közzétett példányt tölti le
    default: -1
    """
    home_dir = Path(homedir)
    url = "https://www.parlament.hu/orszaggyulesi-naplo"
    response = requests.get(url)

    if response.status_code == http.client.OK:

        content = response.text
        soup = BeautifulSoup(content, 'html.parser')

        # get all document links
        links = soup.find_all("a", href=True)

        linklist = [l.get('href') for l in links \
                    if parse.urlparse(l.get('href'))\
                    .path.startswith("/documents/")]
        content_list = [l.get_text() for l in links \
                    if parse.urlparse(l.get('href'))\
                    .path.startswith("/documents/")]

        link_dict = dict(zip(content_list, linklist))

        issue_dict = {}
        for key, value in link_dict.items():
            try:
                key2 = int(key.replace(". szám", ""))
                issue_dict[key2] = value
            except ValueError:
                pass

        if szam == -1:
            latest_issue = issue_dict[max(issue_dict.keys())]
            naplo_url = "https://www.parlament.hu/" \
            + str(latest_issue)
            response = requests.get(naplo_url)
            file_name = max(issue_dict.keys())

        else:
            issue = issue_dict[int(szam)]
            naplo_url = "https://www.parlament.hu/" \
            + str(issue)
            response = requests.get(naplo_url)
            file_name = int(szam)

        with open(home_dir/f"Országgyűlési Napló {file_name}.szám.pdf",
                  'wb') as file:
            file.write(response.content)
            print(f"Országgyűlési Napló {file_name}"\
            f".szám.pdf mentve: {home_dir}")
    else:
        print("Request not succeeded.")

def szam_lista()->list:
    "#TODO"
    url = "https://www.parlament.hu/orszaggyulesi-naplo"
    response = requests.get(url)

    if response.status_code == http.client.OK:
        content = response.text
        soup = BeautifulSoup(content, 'html.parser')

        # get all document links
        links = soup.find_all("a", href=True)
        content_list = [l.get_text() for l in links \
                    if parse.urlparse(l.get('href'))\
                    .path.startswith("/documents/")]
        casted_list = []
        for text in content_list:
            try:
                cleaned = int(text.replace(". szám", ""))
                casted_list.append(cleaned)
            except ValueError:
                pass
    return sorted(casted_list)

def legujabb_szam()->int:
    "#TODO"
    url = "https://www.parlament.hu/orszaggyulesi-naplo"
    response = requests.get(url)

    if response.status_code == http.client.OK:
        content = response.text
        soup = BeautifulSoup(content, 'html.parser')

        # get all document links
        links = soup.find_all("a", href=True)
        content_list = [l.get_text() for l in links \
                    if parse.urlparse(l.get('href'))\
                    .path.startswith("/documents/")]
        casted_list = []
        for text in content_list:
            try:
                cleaned = int(text.replace(". szám", ""))
                casted_list.append(cleaned)
            except ValueError:
                pass
        legujabb = max(casted_list)
    return legujabb
