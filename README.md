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

**python lenta_ru.py --file=”/home/ubuntu/rbc/nicetry/parse_lentaru/lenta_ru.pkl” --rubric=news --date=2020.01.28**
