import os

import requests
from bs4 import BeautifulSoup

from pokemon.models import Nature
from utils import db_utils


def get_nature_info():
    url = os.environ.get('NATURE_URL')
    response = requests.get(url)
    if response.status_code != 200:
        return (None, None, None)
    soup = BeautifulSoup(response.text, 'html.parser')
    tables = soup.find_all('table')
    for table in [(table) for table in tables if table.attrs.get('class') and 'dextable' in table.attrs.get('class')]:
        for row in [tr for tr in table.find_all('tr') if tr.find_all('td')[0].string != 'Natures Name']:
            nature = row.find_all('td')
            yield (nature[0].contents[0].strip(), nature[2].string.strip(), nature[3].string.strip())


def build_natures_db():
    for nature in get_nature_info():
        defaults = {
            'name': nature[0].upper(),
            'positive': nature[1].upper() if nature[1].upper() != "NONE" else None,
            'negative': nature[2].upper() if nature[2].upper() != "NONE" else None
        }
        obj, created = Nature.objects.update_or_create(
            name__iexact=nature[0], defaults=defaults)
        if not created:
            print("Updated {} with {}".format(obj.name, defaults))
