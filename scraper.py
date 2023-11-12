import requests
import re 
from bs4 import BeautifulSoup

def get_psychologist_names_from_avtale(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Dette vil kaste en feil for dårlige statuskoder.
        soup = BeautifulSoup(response.text, 'html.parser')
        names = [name.get_text(strip=True) for name in soup.select('td > a')]
        
        if not names:  # Hvis ingen navn ble funnet, logg HTML for feilsøking.
            with open('html_log.txt', 'w', encoding='utf-8') as file:
                file.write(soup.prettify())

        return names
    except Exception as e:
        print(f"En feil oppstod: {e}")
        return []  # Returnerer en tom liste hvis det oppstår en feil.


def scrape_privatpraktiserende(url):
    response = requests.get(url)
    response.encoding = 'utf-8'
    data_pattern = re.compile(r"info: '(.*?)<\/ul>'")
    matches = data_pattern.findall(response.text)

    oslo_psychologists = []
    for match in matches:
        if 'Oslo' in match:
            soup = BeautifulSoup(match, 'html.parser')
            name_tag = soup.find('h4', class_='map_hfour')
            if name_tag:
                name = name_tag.get_text(strip=True)
                oslo_psychologists.append(name)  # Endret fra set til list for å beholde rekkefølgen

    return oslo_psychologists

    return oslo_psychologists

def scrape_legelisten(base_url):
    all_psychologists = []  # Bruk en liste for å bevare rekkefølgen og håndtere duplikater

    for page in range(1, 94):  # Anta at det er 93 sider å skrape
        url = f"{base_url}{page}"
        response = requests.get(url)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text, 'html.parser')

        # Finn alle navn og adresser på siden
        for row in soup.select('tbody tr[itemscope]'):
            name = row.select_one('.name [itemprop="name"]').get_text(strip=True)
            # Her antar vi at e-post og telefonnummer ikke er tilgjengelige
            psychologist_info = {
                'name': name,
                # 'address': full_address,  # Kommentert ut hvis adressen ikke er nødvendig eller ikke tilgjengelig
                'country': '',
                'language': '',
                'email': None,
                'phone_number': None,
                'profile_picture': '',
                'bio': '',
                'gender_categories': '',
                'status': '',
            }
            all_psychologists.append(psychologist_info)

    return all_psychologists

