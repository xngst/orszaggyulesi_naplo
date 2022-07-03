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

import http.client
import re
import requests
from bs4 import BeautifulSoup
from io import StringIO
from pathlib import Path
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from requests.packages import urllib3
from urllib import parse

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

def pdf_to_txt(path: str)->str:
    "pdf dokumentum parzolása"
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr,
                           laparams=laparams)
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    with open(path, 'rb') as file:
        for page in PDFPage.get_pages(file):
            interpreter.process_page(page)
    text = retstr.getvalue()
    return text

"""
oszággyűlési napló tisztazo modul
"""

def ogy_n_tisztazo(text: str)->str:
    r"""
    eltavolitja:
        - a sorvegi szoelvalasztashoz hasznalt "-" kotojeleket
            peldaul:
                Ország-\n
                gyűlés
                ->
                Országgyűlés!
        - ido jeloleseket,
            peldaul: (9.10)
        - oldalszamokat
            peldaul: 8712
        - oldal fejleceket peldaul:
            "Az Országgyűlés tavaszi ülésszakának 13. ülésnapja,
            2019. április 2-án, kedden"
    """
    dash_pat = re.compile(r'-\n')
    time_stamp_pat = re.compile(r" \n\n \(\d{2}.\d{2}\) \n\n \n")
    page_number_pat = re.compile(r'\n\n\x0c\d{4,5}|\n\n\d{5}')
    header_pat = re.compile(r'\n\nAz Országgyűlés(.*)ülés(.*)\n')

    cleaned_text = re.sub(dash_pat, '', text)
    cleaned_text = re.sub(time_stamp_pat, '', cleaned_text)
    cleaned_text = re.sub(page_number_pat, '', cleaned_text)
    cleaned_text = re.sub(header_pat, '', cleaned_text)

    cleaned_text = cleaned_text.replace("  ", " ").replace("  ", " ")
    cleaned_text = cleaned_text.replace("\n", " ")

    return cleaned_text

def szam(text: str)->str:
    try:
        szam_pat = re.compile(r"\d{2,3}\. szám")
        szam = re.findall(szam_pat, text)
        szam = szam[0].replace(". szám","").strip()
    except IndexError as IE:
        szam_pat = re.compile(r"\d{1,3}/\d{1,2}\. szám")
        szam = re.findall(szam_pat, text)
        szam = szam[0].replace(". szám","").strip()
        pass
    return szam

def ciklus(text: str)->str:
    ciklus_pat = re.compile(r"[\d+]{4,4}-[\d+]{4,4}. országgyűlési ciklus")
    ciklus_result = re.findall(ciklus_pat, text)
    ciklus_clean = ciklus_result[0].replace(". országgyűlési ciklus", "")
    return ciklus_clean

def ules_datum(text: str)->str:
    date_pattern = re.compile(r"([\d+]{4,}\.\s[\w+]{5,10}\s[\d+]{1,2}\.)")
    date_list = re.findall(date_pattern, text)[0]
    return date_list

def elnok_lista(text: str)->list:
    chairman_pattern = re.compile("Napló (.*) elnöklete alatt")
    chairman_list = re.findall(chairman_pattern, text)
    chairman_list = chairman_list[0].split("és")
    chairman_list = [i.strip() for i in chairman_list]
    return chairman_list

def jegyzo_lista(text: str)->list:
    notary_pattern = re.compile("Jegyzők:(.*)Hasáb")
    notary_list = re.findall(notary_pattern, text)
    notary_list = notary_list[0].replace("  ", "")\
    .replace(" \x0c", "").split(",")
    notary_list = [i.strip() for i in notary_list]
    return notary_list

def torzs_szoveg(text: str)->str:
    first_page = re.compile(r"ELNÖK:")
    ogy_start = re.search(first_page, text).start()
    ogy_end = text.find("ülésnapot bezárom.")
    main_text = text[ogy_start:ogy_end-4]
    return main_text

def torveny_javaslat_lista(text: str)->list:
    motion_pattern = re.compile(r"T/\d+")
    motion_list = sorted(list(set(re.findall(motion_pattern, text))))
    return motion_list

def hatarozati_javaslat_lista(text: str)->list:
    proposal_pattern = re.compile(r"H/\d+")
    proposal_list = sorted(re.findall(proposal_pattern, text))
    return proposal_list

def kepviselo_lista(text: str)->list:
    mp_name_pattern = re.compile(r"(\b[A-Z.ÁÍÉÓÖŐÚÜŰ-]+)"\
                                 r"(\s[A-Z.ÁÍÉÓÖŐÚÜŰ-]+)"\
                                 r"(\s[A-Z.ÁÍÉÓÖŐÚÜŰ-]+)?"\
                                 r"(\s[A-Z.ÁÍÉÓÖŐÚÜŰ-]+)*")
    mp_matches = re.findall(mp_name_pattern, text)
    mp_list = []
    for name in mp_matches:
        joined_name = "".join(name)
        if len(joined_name) > 8:
            mp_list.append(joined_name)
    mp_list = list(sorted(set(mp_list)))
    return mp_list

def kepviseloi_felszolalas_szotar(text: str, mp_list: list)->dict:
    name_dict = {}
    for name in mp_list:
        name_dict[name] = [name.start() for name in re.finditer(name, text)]
    mp_speech_dict = {}
    for name, start_char in name_dict.items():
        if start_char:
            if len(start_char) > 1:
                speech_list = []
                for value in start_char:
                    end_char = text[value:].find("ELNÖK:")
                    speech = text[value:value + end_char]
                    speech_list.append(speech)
                    mp_speech_dict[name] = speech_list
            else:
                end_char = text[start_char[0]:].find("ELNÖK:")
                speech = text[start_char[0]:start_char[0] + end_char]
                mp_speech_dict[name] = speech
    return mp_speech_dict

def reakcio_lista(text: str)->list:
    emot_pat = re.compile(r"\([A-ZÁÍÉÓÖŐÚÜŰ a-z áíéóöőúüű.…,:!?-]+\)")
    emot_list = re.findall(emot_pat, text)
    emot_list = [i for i in emot_list if len(i) > 8]
    return emot_list

def reakcio_szotar(kepviseloi_felszolalas_szotar):
    reakcio_szotar = {}
    for key, value in kepviseloi_felszolalas_szotar.items():
        reakcio_szotar[key] = [reakcio_lista(i) for i in value if reakcio_lista(i)]
    return reakcio_szotar

class ogy_naplo:
    """
    Osztaly az orzsaggyulesi naplo konnyebb kezelesehez
    naplo = ogy_naplo(file_eleresi_utvonal)
    """
    def __init__(self, path):
        self.path = path
        self.text = pdf_to_txt(path)
        self.tisztazott = ogy_n_tisztazo(self.text)
        self.torzs_szoveg = torzs_szoveg(self.tisztazott)
        self.szam = szam(self.tisztazott)
        self.ciklus = ciklus(self.tisztazott)
        self.ules_datum = ules_datum(self.tisztazott)
        self.elnok_lista = elnok_lista(self.tisztazott)
        self.jegyzo_lista = jegyzo_lista(self.tisztazott)
        self.torvenyjavaslatok = \
        torveny_javaslat_lista(self.torzs_szoveg)
        self.hatarozati_javaslat_lista = \
        hatarozati_javaslat_lista(self.torzs_szoveg)
        self.kepviselo_lista = kepviselo_lista(self.torzs_szoveg)
        self.kepviseloi_felszolalas_szotar = \
        kepviseloi_felszolalas_szotar(self.torzs_szoveg, self.kepviselo_lista)
        self.reakcio_szotar = \
        reakcio_szotar(self.kepviseloi_felszolalas_szotar)
