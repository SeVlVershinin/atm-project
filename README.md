# Определение популярности геолокации для размещения банкомата (МОВС-2023, годовой проект)
## Описание проекта
В рамках проекта решается задача прогнозирования индекса популярности банкомата по географическим координатам места его размещения. Задача ранее решалась на новогоднем чемпионате по анализу данных [Happy Data Year](https://boosters.pro/championship/rosbank2/overview). 
Предложенные на чемпионате данные о геопозиции банкоматов и их индексе популярности (целевая переменная) взяты за 
основу и расширены дополнительной информацией о структуре адреса (населенный пункт, улица и т.п.), площади населенного 
пункта и численности его населения, а также о количестве точек интереса (магазинов, остановок, аптек, других банкоматов 
и т.п.), полученной с помощью сервисов [dadata](dadata.ru), [GeoTree](https://geotree.ru/features), а также из базы данных [Open Street Map](https://www.openstreetmap.org).

## Продукт
В ходе выполнения проекта разработан продукт, позволяющий получать прогнозы индексов популярности для банкоматов в заданных точках размещения. Продукт включает в себя: 
- реализованный с использованием библиотеки FastAPI ML-сервис, который по координатам потенциального места размещения банкомата получает у сторонних сервисов дополнительные характеристики места, после с использованием базе ранее обученной модели выполняет предсказание индекса популярности; 
- Telegram-бот, предоставляющий пользователю простой интерфейс взаимодействия с сервисом получения прогнозов. 

__Подробное описание продукта приведено на [отдельной странице](product.md).__


## Текущие результаты работ:
На текущий момент: 
- разработан конвейер обогащения обучающей выборки и входных данных пользователя дополнительными данными, перечисленными
выше (пакет [data_collection](data_collection)); 
- выполнен разведочный анализ обогащенной обучающей выборки ([jupyter notebook](eda/eda.ipynb));
- проведено обучение, оценка качества и выбор лучшей из различных моделей машинного обучения для решения задачи 
([jupyter notebook](prediction_model/prediction_model.ipynb));
- на основе лучшей модели разработан сервис предсказания популярности банкомата (пакет [predicition-service](prediction-service))
и телеграм-бот для взаимодействия с ним (пакет [tg-bot](tg-bot)); 
- на базе github actions настроен автоматизированный CD-pipeline, формирующий docker-образы с [сервисом предсказаний](https://hub.docker.com/repository/docker/sevlvershinin/atm-project-api/) 
и [телеграм-ботом](https://hub.docker.com/repository/docker/sevlvershinin/atm-project-bot/) и размещающий их на Docker Hub; 
- экземпляры сервиса предсказаний и телеграм-бота с помощью ```docker compose``` на вирутальной машине в сети Интернет. 

Ссылки: 
- docker-образы сервиса предсказаний и телеграм-бота: [prediction-service](https://hub.docker.com/repository/docker/sevlvershinin/atm-project-api/) 
и [telegram-bot](https://hub.docker.com/repository/docker/sevlvershinin/atm-project-bot/)
- API сервиса предсказаний: http://94.139.242.35/docs
- телеграм-бот: [ATM project bot (HSE)](https://t.me/atm_project_bot)

## Состав команды
 - Алина Лукманова
 - Антон Зайцев
 - Сергей Вершинин

Куратор: Елизавета Гаврилова

