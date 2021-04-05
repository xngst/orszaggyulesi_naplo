"""
oszággyűlési napló tisztazo modul
"""

import re

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
    page_number_pat = re.compile(r'\n\n\x0c\d{5}|\n\n\d{5}')
    header_pat = re.compile(r'\n\nAz Országgyűlés(.*)ülés(.*)\n')

    cleaned_text = re.sub(dash_pat, '', text)
    cleaned_text = re.sub(time_stamp_pat, '', cleaned_text)
    cleaned_text = re.sub(page_number_pat, '', cleaned_text)
    cleaned_text = re.sub(header_pat, '', cleaned_text)

    cleaned_text = cleaned_text.replace("  ", " ")
    cleaned_text = cleaned_text.replace("\n", " ")

    return cleaned_text
