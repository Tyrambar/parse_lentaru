**EN: It's an old task for some interview in 2020 in Moscow.**

Python version: 3.7.5
Recommended: use a virtual environment.

Install dependencies : **pip install -r req.txt**

**What it does**

This script parses articles (by using BeautifulSoup) from lenta.ru filtered by date and/or section (called “rubric” on Lenta).
Results are stored in a pickle file. You are able to create a new file or update an existing one.

All parameters are optional.

**Parameters & behavior**

*--date* — articles for that date are collected by sections (rubrics), including full articles text.

*--rubric* (aka section/category) — when provided:
a) *Without --date*: collects articles for the given rubric, excluding article text.
b) *With --date*: collects articles for that date and rubric, including article text.

*--file* — path to the pickle file to create or update.

**Example**

**python lenta_ru.py --file=”/home/ubuntu/parse_lentaru/lenta_ru.pkl” --rubric=news --date=2020.01.28**


**RU: Старая тестовая задача для одного из интервью в 2020 году в Москве**
Рекомендуется перед выполнением программы загрузить отдельное виртуальное окружение.

Программа выполнена на Python 3.7.5
Установка необходимых пакетов: **pip install -r req.txt**
Пользоваться программой рекомендуется в системах UNIX для корректной работы.

Программа парсит статьи с сайта lenta.ru, согласно заданным параметрам даты и рубрики статей, 
и сохраняет данные в pickle файл, с возможностью перезаписи/дополнения в файл. 
Параметры даты и рубрики необязательны.

**При задании параметра даты:** могут быть выведены статьи указанных рубрик или всех рубрик(news/articles), включая текст статей;

**При задании параметра рубрики:** при отсутствии параметра даты собирает статьи по указанным рубрикам(или по всем), исключая текст статей;
при наличии даты всегда включает сбор текста статей.

***Пример запроса:***

**python lenta_ru.py --file=”/home/ubuntu/parse_lentaru/lenta_ru.pkl” --rubric=news --date=2020.01.28**
