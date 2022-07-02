"""
scraper 
Letölti a https://www.parlament.hu/orszaggyulesi-naplo 
oldalon pdf formátumban közzétett országgyűlési naplókat.

szam_lista
Visszaadja az adott ciklusban közzétett 
összes parlamenti napló sorszámait.

legujabb_szam
Visszaadja az adott ciklusban közzétett 
legutolsó parlementi napló számát
"""

from urllib import parse
from pathlib import Path

import http.client
import requests

from bs4 import BeautifulSoup

from requests.packages import urllib3
urllib3.disable_warnings()

def scraper(homedir: str, szam: int = -1)->str:
    """
    Letölti a szám paraméterrel meghatározott parlamenti naplót 
    a homedir paraméterben megadott könyvtárba.
    szam: kiadvány száma pozitív integer
    ha szam = -1 (default), akkor a legutoljára közzétett példányt tölti le
    """
    home_dir = Path(homedir)
    url = "https://www.parlament.hu/orszaggyulesi-naplo"
    response = requests.get(url, verify=False)

    if response.status_code == http.client.OK:

        content = response.text
        soup = BeautifulSoup(content, 'html.parser')

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

        with open(home_dir/f"Országgyűlési Napló {file_name}.szám.pdf",'wb') as file:
            file.write(response.content)
            print(f"Országgyűlési Napló {file_name}"\
            f".szám.pdf mentve: {home_dir}")
    else:
        print("Request not succeeded.")

def szam_lista()->list:
    """
    Visszaadja az adott ciklusban közzétett 
    összes parlamenti napló sorszámait.
    """
    url = "https://www.parlament.hu/orszaggyulesi-naplo"
    response = requests.get(url,verify=False)

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
            except ValueError as VE:
                print(VE)
                pass
    return sorted(casted_list)

def legujabb_szam()->int:
    """
    Visszaadja az adott ciklusban közzétett 
    legutolsó parlementi napló számát
    """
    url = "https://www.parlament.hu/orszaggyulesi-naplo"
    response = requests.get(url,verify=False)

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
            except ValueError as VE:
                print(VE)
                pass
        legujabb = max(casted_list)
    return legujabb
