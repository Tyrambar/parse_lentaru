from bs4 import BeautifulSoup as Bs
import pickle
import requests
from typing import NamedTuple
import sys
import argparse

from random import choice
import re

from additional_const import *
from datetime import datetime


MAIN_URL = 'https://lenta.ru'
USERAGENT = {'User-agent': choice(USERAGENTS)}
ART_TAGS = {
    'news': 'item news b-tabloid__topic_news',
    'articles': 'item article'
}
ALL_ART = []


class Art(NamedTuple):
    rubric : int
    title : str
    link : str
    date : datetime

    def __str__(self):
        return ('Новость: ' if self.rubric == 'news' else 'Статья: ') + \
               self.title + datetime.strftime(self.date, ' %d.%m.%Y')

def createParser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file', required=True)
    parser.add_argument('-r', '--rubric', default=None)
    parser.add_argument('-d', '--date', default=None)

    return parser

def to_format_date(raw_date):
    if raw_date[5] != ' ':
        raw_date = raw_date[:5] + ' ' + raw_date[5:]
    date_spl = re.sub('—', '', raw_date).split()
    if date_spl[-1].lower() == 'сегодня':
        format_date = ' '.join(date_spl[:-1]) + \
                      datetime.strftime(datetime.today(), ' %d %m %Y')
    else:
        if date_url[:4] != '2020':
            format_date = ' '.join(date_spl[:-2] + [MONTHS[date_spl[-2]]] + [date_spl[-1]])
        else:
            format_date = ' '.join(date_spl[:-1] + [MONTHS[date_spl[-1]]] +
                                   [str(datetime.today().year)])
    return format_date

def get_art_rubric(rubric_url, date_url):
    req = requests.get(f'{MAIN_URL}/{rubric_url}/{date_url}', headers=USERAGENT)
    bs = Bs(req.text, "html.parser")
    with open(path_file, 'wb') as art_pkl:
        if rubric_url == 'all':
            rubrics = (ART_TAGS['news'], ART_TAGS['articles'])
        else:
            rubrics = (ART_TAGS[rubric_url], )
        for rubric in rubrics:
            all_raw_art = bs.find_all("div", class_=rubric)
            for raw_art in all_raw_art:
                date = raw_art.find("span", class_='g-date item__date').get_text()
                title_art = raw_art.find("div", class_="titles").find('a')
                art = Art(
                    rubric = rubric_url,
                    title = title_art.get_text(),
                    link = title_art.get('href'),
                    date = datetime.strptime(to_format_date(date), '%H:%M %d %m %Y')
                )
                if date_url:
                    ALL_ART.append(art)
                else:
                    pickle.dump(art, art_pkl)
                print(art)
        if date_url:
            ALL_ART.sort(key= lambda element: element.date)
            #for sort_art in ALL_ART:
            #    pickle.dump(sort_art, art_pkl)
            pickle.dump(tuple(ALL_ART), art_pkl)


if __name__ == '__main__':
    parser = createParser()
    namespace = parser.parse_args(sys.argv[1:])
    print(namespace)
    path_file = namespace.file[1:-1]
    rubric_url = namespace.rubric if namespace.rubric else 'all'
    print(rubric_url)
    date_url = '/'.join(namespace.date.split('.'))
    get_art_rubric(rubric_url, date_url)
