# Определение популярности геолокации для размещения банкомата (МОВС-2023, годовой проект)
## Описание проекта
В рамках проекта разрабатывается модель, которая по географическим координатам определит оценку индекса популярности банкомата в этой локации. Задача ранее решалась 
на новогоднем чемпионате по анализу данных [Happy Data Year](https://boosters.pro/championship/rosbank2/overview). Предложенные на чемпионате данные о геопозиции банкоматов и их индексе популярности (целевая переменная) взяты за основу и расширены дополнительной информацией о структуре адреса (населенный пункт, улица и т.п.), полученной с помощью сервиса [dadata](dadata.ru)

## Описание набора данных
Описание набора данных, полученного расширением исходного набора данными сервиса [dadata](dadata.ru), находится в следующих Jupyter Notebooks
- [Анализ городов по количеству банкоматов](https://github.com/SeVlVershinin/atm-project/blob/main/data_collection/ATM%20distribution%20by%20city.ipynb)
- [Анализ корреляции признаков и анализ признака atm_group](/tree/main/data_collection/Feature analysis.ipynb)
- [Описание данных датасета (исходного и преобразованного)](/tree/main/data_collection/Dataset description.ipynb)
- [Отображение банкоматов на карте](https://github.com/SeVlVershinin/atm-project/blob/main/data_collection/ATM%20on%20map.ipynb)

Код, использованные для расширения исходного набора данных содержится в каталоге [data_collection](/tree/main/data_collection) 

## Текущий план работ 

--- **до 22.10.2023** --- 
 - завершить наполнение датасета данными из дадаты (проблемы пустых полей, проблемы адресов в транслитерации) 
 - ~~завести аккаунт на github, создать readme.md в соответствии с требования чекпойнта~~
 - выложить на github датасет и код, с помощью которого делали наполнение доп.данными
 - сообщить куратору, создать общую группу в Telegram

--- **до 31.10.2023** ---  (чекпойнт №1)
 - обсудить с куратором и зафиксировать примерный план работ по проекту
 - добавить ссылку на репозиторий в общую таблицу проектов МОВС23 (когда такая таблица будет)
 
## Состав команды
 - Алина Лукманова
 - Антон Зайцев
 - Сергей Вершинин

Куратор: Елизавета Гаврилова

## Дополнительно
[Описание процесса разработки](dev_process.md)
