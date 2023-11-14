# Определение популярности геолокации для размещения банкомата (МОВС-2023, годовой проект)
## Описание проекта
В рамках проекта разрабатывается модель, которая по географическим координатам определит оценку индекса популярности банкомата в этой локации. Задача ранее решалась 
на новогоднем чемпионате по анализу данных [Happy Data Year](https://boosters.pro/championship/rosbank2/overview). Предложенные на чемпионате данные о геопозиции банкоматов и их индексе популярности (целевая переменная) взяты за основу и расширены дополнительной информацией о структуре адреса (населенный пункт, улица и т.п.), полученной с помощью сервиса [dadata](dadata.ru)

## Описание набора данных
Описание набора данных, полученного расширением исходного набора данными сервиса [dadata](dadata.ru), находится в следующих Jupyter Notebooks:
- [Описание данных датасета (исходного и преобразованного)](https://github.com/SeVlVershinin/atm-project/blob/main/data_collection/notebooks/dataset_description.ipynb)
- [Отображение банкоматов на карте](https://github.com/SeVlVershinin/atm-project/blob/main/data_collection/notebooks/atm_on_map.ipynb)
- [Анализ городов по количеству банкоматов](https://github.com/SeVlVershinin/atm-project/blob/main/data_collection/notebooks/atm_distribution_by_city.ipynb)
- [Анализ корреляции признаков и анализ признака atm_group](https://github.com/SeVlVershinin/atm-project/blob/main/data_collection/notebooks/feature_analysis.ipynb)

Код, использованный для расширения исходного набора данных данными, содержится в каталоге [data_collection/commands](https://github.com/SeVlVershinin/atm-project/tree/main/data_collection/commands) и содержит следующие скрипты:

- *с использованием данных сервиса [dadata](dadata.ru):*
    - [получение дополнительных геоданных по координатам банкоматов](https://github.com/SeVlVershinin/atm-project/blob/main/data_collection/commands/get_dataset_with_additional_geodata.py)
    - [получение координат улиц, районов, городов на основе ФИАС кодов адресов](https://github.com/SeVlVershinin/atm-project/blob/main/data_collection/commands/add_geo_coordinates_to_dataset.py)
    - [уточнение геоданных для записей с уровнем ФИАС меньше 8](https://github.com/SeVlVershinin/atm-project/blob/main/data_collection/commands/clarify_geo_data_for_fias_level_below_8.py)
    - [получение информации по ближайшим станциям метро](https://github.com/SeVlVershinin/atm-project/blob/main/data_collection/commands/add_metro_geo_data_for_cities.py)
    - [получение наименований улиц и номеров домов по кодам ФИАС](https://github.com/SeVlVershinin/atm-project/blob/main/data_collection/commands/add_houses_and_streets_geo_data.py)

- *с использованием данных сервиса [Geotree.ru](https://geotree.ru/):*
    - [получение численности населения и площадей населенных пунктов](https://github.com/SeVlVershinin/atm-project/blob/main/data_collection/commands/add_population_and_area_data_to_dataset.py)

- *с использованием данных [Open Street Map](https://www.openstreetmap.org):*
    - (проект) [получение точек интереса из дампа OSM](https://github.com/SeVlVershinin/atm-project/blob/main/data_collection/notebooks/dataset_extension_with_poi_from_osm.ipynb)


## Текущий план работ 

--- **до 31.10.2023** ---  (чекпойнт №1)
 - обсудить с куратором и зафиксировать примерный план работ по проекту
 
## Состав команды
 - Алина Лукманова
 - Антон Зайцев
 - Сергей Вершинин

Куратор: Елизавета Гаврилова

## Дополнительно
[Описание процесса разработки](dev_process.md)
