"""
országgnyűlési napló parser
#TODO
"""

import re

def szam(text: str)->str:
    ""
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
    """
    #TODO
    """
    ciklus_pat = re.compile(r"[\d+]{4,4}-[\d+]{4,4}. országgyűlési ciklus")
    ciklus_result = re.findall(ciklus_pat, text)
    ciklus_clean = ciklus_result[0].replace(". országgyűlési ciklus", "")
    return ciklus_clean

def ules_datum(text: str)->str:
    """
    #TODO
    """
    date_pattern = re.compile(r"([\d+]{4,}\.\s[\w+]{5,10}\s[\d+]{1,2}\.)")
    date_list = re.findall(date_pattern, text)[0]
    return date_list

def elnok_lista(text: str)->list:
    """
    #TODO
    """
    chairman_pattern = re.compile("Napló (.*) elnöklete alatt")
    chairman_list = re.findall(chairman_pattern, text)
    chairman_list = chairman_list[0].split("és")
    chairman_list = [i.strip() for i in chairman_list]
    return chairman_list

def jegyzo_lista(text: str)->list:
    """
    #TODO
    """
    notary_pattern = re.compile("Jegyzők:(.*)Hasáb")
    notary_list = re.findall(notary_pattern, text)
    notary_list = notary_list[0].replace("  ", "")\
    .replace(" \x0c", "").split(",")
    notary_list = [i.strip() for i in notary_list]
    return notary_list

def torzs_szoveg(text: str)->str:
    """
    #TODO
    """
    first_page = re.compile(r"ELNÖK:")
    ogy_start = re.search(first_page, text).start()
    ogy_end = text.find("Az ülésnapot bezárom.")
    main_text = text[ogy_start:ogy_end]
    return main_text

def torveny_javaslat_lista(text: str)->list:
    """
    #TODO
    """
    motion_pattern = re.compile(r"T/\d+")
    motion_list = sorted(list(set(re.findall(motion_pattern, text))))
    return motion_list

def hatarozati_javaslat_lista(text: str)->list:
    """
    #TODO
    """
    proposal_pattern = re.compile(r"H/\d+")
    proposal_list = sorted(re.findall(proposal_pattern, text))
    return proposal_list

def kepviselo_lista(text: str)->list:
    """
    #TODO
    """
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
    """
    :returns: dict with mp name as key and speech list as value
    """
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
    """
    #TODO
    """
    emot_pat = re.compile(r"\([A-ZÁÍÉÓÖŐÚÜŰ a-z áíéóöőúüű.…,:!?-]+\)")
    emot_list = re.findall(emot_pat, text)
    emot_list = [i for i in emot_list if len(i) > 8]
    return emot_list
