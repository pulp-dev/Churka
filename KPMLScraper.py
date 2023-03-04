import asyncio

import re
import requests
from bs4 import BeautifulSoup

from pprint import pprint
import datetime as dt


URL = 'https://kpml.ru/pages/raspisanie/izmeneniya-v-raspisanii'
DOMAIN = 'https://kpml.ru'


class Scraper:
    def __init__(self):
        self.r = requests.get(URL)
        self.DOMAIN = DOMAIN

    @staticmethod
    def form_name():
        if dt.datetime.today().weekday() == 5:
            delta = 2
        else:
            delta = 1
        d = (dt.date.today() + dt.timedelta(days=delta)).day
        if int(d) < 10:
            d = '0' + str(d)
        m = (dt.date.today() + dt.timedelta(days=delta)).month
        if int(m) < 10:
            m = '0' + str(m)
        name = d + '.' + m + '.pdf'
        return name

    def get_timetables_elements(self):
        soup = BeautifulSoup(self.r.text, 'html.parser')
        elements = soup.findAll("p", attrs={'style': re.compile("line-height: 16px;.*")})
        return self.process_timetables_element(elements)

    def process_timetables_element(self, elements):
        for _ in elements:
            el = _.findAll("a")[0]
            doc = {
                'text': el.text,
                'url': el.get('href'),
            }
            if self.process_doc(doc):
                print(f'timetable for {(dt.datetime.today()  + dt.timedelta(days=1)).date()} have been just saved')
                return f"timetable{self.form_name()}"
        return None

    def process_doc(self, doc):
        # valid grade
        if not ('9-11' in doc['text']):
            return False
        if not (self.form_name() in doc["text"]):
            return False
        pdf_url = self.DOMAIN + doc["url"]

        response = requests.get(pdf_url)

        with open(r"TimeTables/timetable" + self.form_name(), 'wb') as f:
            f.write(response.content)
        return True

