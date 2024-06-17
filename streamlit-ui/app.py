import pandas as pd
import streamlit as st
from PIL import Image
from model import open_data, preprocess_data, split_data, load_model_and_predict
import folium
from streamlit_folium import st_folium

import json
import requests
from pydantic import BaseModel

HEADERS = {'Content-type': 'application/json', 'accept': 'application/json'}
first_render = True

class AtmData(BaseModel):
    lat: float
    lon: float
    atm_group: str

atms = pd.read_csv('streamlit_demo/data/train.csv')

def process_main_page():
    #show_main_page()
    render_page()
    #process_side_bar_inputs()


def show_main_page():
    image = Image.open('streamlit_demo/data/banks.jpg', width=1000)

    st.set_page_config(
        layout="wide",
        initial_sidebar_state="auto",
        page_title="Banks",
        page_icon=image,

    )

    st.write(
        """
        # Определение индекса популярности банкомата
        """
    )

    st.image(image)


def write_user_data(df):
    st.write("## Данные банкомата")
    st.write(df)


def write_prediction(prediction, prediction_probas):
    st.write("## Предсказание")
    st.write(prediction)

    st.write("## Вероятность предсказания")
    st.write(prediction_probas)


def process_side_bar_inputs():
    st.sidebar.header('Параметры банкомата')
    user_input_df = sidebar_input_features()


   # prediction, prediction_probas = load_model_and_predict(user_X_df)
    #write_prediction(prediction, prediction_probas)


def render_page():
    st.set_page_config(
        layout='wide',
        page_title="Определение индекса популярности банкоматов"
    )

    st.header('Определение индекса популярности банкоматов')
    #st.subheader('Разведочный анализ данных')

    bank_image = Image.open('streamlit_demo/data/banks.jpg')
    st.image(
        bank_image,
        width=1000
    )

    tab1, tab2, tab3, tab4 = st.tabs(
        ["EDA",
         "EDA после обогащения",
         "Предсказания",
         "ОСНОВНЫЕ ВЫВОДЫ"
         ])

    with tab1:
        render_tab1()
    with tab2:
        render_tab2()
    with tab3:
        render_tab3()
    with tab4:
        render_tab4()


def render_tab1():
    st.markdown("""
    ##### EDA
    """)
    #st.dataframe(clients)
    st.markdown("""
    ##### Описание признаков

    Набор данных включает в себя следующие характеристики банкомата:
    """)
    st.markdown(
        """
    - id_0 - порядковый номер в полученном датасете 
- id - предположительно, порядковый номер в исходном датасете, который потом был разбит на части, одной из которых стал полученный нами датасет
- atm_group - банковская группа, которой принадлежит банкомат
- address - адрес банкомата в транслитерации
- addres_rus - адрес банкомата на русском
- lat, long - широта и долгота, координаты расположения банкомата на карте
- target - целевая переменная, индекс популярности места для расположения банкомата
- элементы адреса, полученны в результате анализа исходного адреса или координат банкомата: 
    - federal_district - федеральный округ РФ
    - region_with_type - субъект РФ
    - area_with_type - муниципальный район или городской округ в составе субъекта РФ
    - city_with_type - город
    - city_area - административный округ города (для г.Москва)
    - city_district_with_type - район города
    - settlement_with_type - сельское поселение (в составе муниципального района или городского округа)
    - street_with_type - улица
    - house - номер дома
- capital_marker - признак столицы региона или города федерального значения
    - 1 — центр района (Московская обл, Одинцовский р-н, г Одинцово)
    - 2 — центр региона (Новосибирская обл, г Новосибирск)
    - 3 — центр района и региона (Томская обл, г Томск)
    - 4 — центральный район региона (Тюменская обл, Тюменский р-н)
    - 0 — ничего из перечисленного (Московская обл, г Балашиха)
- данные о ближайших станциях и линиях метро: 
    - nearest_metro_distance - расстояние до ближайшего метро
    - metro_station_name_{N}, metro_line_name_{N}, metro_distance_{N} - наименование станции, ветки и расстояния до станции метро N (N - не более 3)
- locality_area - площадь города, в котором расположен банкомат (в кв.км)
- locality_population - население города, в котором расположен банкомат (количество человек)
        """
    )
    gr1_col_list = ['atm_group', 'lat', 'long', 'target', 'capital_marker', 'locality_area', 'locality_population']
    df = atms[gr1_col_list]
    description = df.describe(include='all')
    description['locality_population'] = description['locality_population'].apply("{0:.5f}".format)
    description['locality_area'] = description['locality_area'].apply("{0:.5f}".format)

    st.dataframe(description)
    st.markdown(
        """
    - в столбцах atm_group и target пропусков нет
    - в столбцах lat и lon пропущено одно значение (видимо, для одного банкомата отсутствуют координаты)
    - в столбцах locality_area и locality_population:
                - есть ~ 100 пропусков
                - есть нулевые значения, что не очень логично, т.к. население и площадь населенного пункта не могут быть нулевой
максимальное значение количества населения выглядит правдоподобно (очевидно, это Москва с ее ~ 12 милионным населением), а вот максимальная площадь в ~3 миллиона кв.км. не очень похожа на площадь города и требует отдельного внимания
        """)

    #image = Image.open('streamlit_demo/data/banks.jpg', width=1000)

    #st.image('streamlit_demo/data/atm_group.jpg', width=1000)

    st.image('streamlit_demo/data/coords.jpg', width=1000)
    st.markdown(
        """
        Основные значения широты находятся в окрестности 55, а основные значения долготы в окрестностях 30, 80 и 130, что примерно соответствует расположению основных населенных пунктов на территории РФ
        """
    )

    st.image('streamlit_demo/data/city.jpg', width=1000)

    st.markdown(
        """
        Основная часть данных приходятся города с численностью населения до 1 миллиона человек. Кроме того, имеется два всплеска на отметках ~ 5 млн.чел. (это Санкт-Петербург) и ~12 млн.чел. (это Москва)
        """
    )

    st.image('streamlit_demo/data/popularity.jpg', width=1000)
    st.markdown(
        """
        Наибольшей популярностью пользуются банкоматы Росбанка и Альфабанка
        """
    )

    st.image('streamlit_demo/data/map.jpg', width=1500)
    st.markdown(
        """
        Чем банкомат находится восточнее или севернее, тем он более привлекателен для пользователей.
        """
    )




def render_tab3():
    st.markdown(
        """
        #### Предсказание 

        """
    )
    atm_group = st.selectbox("Банк", (
    "Rosbank", "AkBars", "Alfabank", "Gazprombank", "Raiffeisen", "Rosselkhozbank", "Uralsib"))

    line = st.divider()
    st.caption("Координаты банкомата")

    x_coord = st.number_input("Широта",55.8)
    y_coord = st.number_input("Долгота", 37.6)

    #st.caption("Город, улица, номер дома через пробел (Москва Сухонская 11)")
    #address = st.text_input("Адрес банкомата:")

    pred = predict_one(AtmData(lat = x_coord, lon = y_coord, atm_group=atm_group))
    #pred = 1
    st.write("### Отображение на карте")
    st.write(pred)
    #st.write(f'Индекс популярности= {pred:.4f}')

    m = folium.Map(location=[x_coord, y_coord], zoom_start=15)
    folium.Marker(
        [x_coord, y_coord], popup=f"индекс популярности= {pred:.4f}", tooltip=atm_group
    ).add_to(m)

    st_data = st_folium(m, width=1500)

def render_tab2():
    st.markdown("""
    ##### EDA после обогащения данных
    """)
    #st.dataframe(clients)
    st.markdown("""
    ##### Описание новых признаков
    - sustenance - общественное питание,
    - education - образовательные учреждения
    - fuel - заправочные станции
    - car_service - автосервис
    - parking_space - парковки
    - atm - банкоматы
    - bank - банки
    - bureau_de_change - обмен валюты
    - outpatient_medical_facilities - больницы
    - inplace_medical_facilities - медицинские учреждения
    - pharmacy - аптеки
    - veterinary - ветеринарии
    - entertainment - развлечения
    - entertainment_for_adults - развлечения для взрослых
    - administrative_buildings - административные здания
    - police - полиция
    - fire_station - пожарная станция
    - post_office - почта
    - marketplace - рынок
    - public_transport_stop_position - остановка общественного транспорта
    - alcohol_shop - алкогольных магазин
    - food_shop - продуктовый магазин
    - supermarket - супермаркет
    - mall - торговый центр
    - clothing_shop - магазин одежды
    - beauty_store - магазин косметики
    - electronics_store - магазин электроники
    - sport_store - магазин спортивных товаров
    - auto_moto_store - магазин автозапчастей
    - car_parts_store - продажа машин
    - hobbies_store - магазины для хобби
    - books_store - книжный магазин
    - hotel - отель
    - museum - музей

    """)


    st.image('streamlit_demo/data/points.jpg', width=1000)

    st.markdown(
        """
        Матрица корреляции целевой переменной и точек интереса
        """
    )

    st.image('streamlit_demo/data/corr.jpg', width=1500)

    st.markdown(
        """
        Наибольшую корреляцию с целевой переменной имеют поля: магазины косметики, магазины электроники, магазины для хобби.
        """
    )
def render_tab4():
    st.markdown(
        """
        #### Основные выводы 

        """
    )

def sidebar_input_features():
    atm_group = st.sidebar.selectbox("Банк", ("Rosbank", "AkBars", "Alfabank", "Gazprombank", "Raiffeisen", "Rosselkhozbank", "Uralsib"))

    line = st.sidebar.divider()
    st.sidebar.caption("Координаты банкомата")
    x_coord = st.sidebar.number_input("X координата")
    y_coord = st.sidebar.number_input("Y координата")

    st.sidebar.caption("Город, улица, номер дома через пробел (Москва Сухонская 11)")
    address = st.sidebar.text_input("Адрес банкомата:")


    data = {
        "x_coord": x_coord,
        "y_coord": y_coord,
        "address": address,
    }

    pred = calculate_target(x_coord, y_coord, address)
    st.write("### Предсказание популярности")
    st.write(pred)

    #m = folium.Map(location=[39.949610, -75.150282], zoom_start=16)
    m = folium.Map(location=[60.940995, 112.738319], zoom_start=5)
    m = folium.Map(location=[x_coord, y_coord], zoom_start=10)
    folium.Marker(
        [x_coord, y_coord], popup=atm_group, tooltip= atm_group
    ).add_to(m)


    map = folium.Map(location=[46.940995, 142.738319], zoom_start=3)

    # Создание кругового маркера
    folium.CircleMarker(
        location=[x_coord, y_coord],
        radius=50,  # радиус в метрах
        color='blue',
        fill=True,
        fill_opacity=0.5
    ).add_to(map)

    # call to render Folium map in Streamlit
    st_data = st_folium(m, width=1500)
    #st.write(map)
    st.write(x_coord, y_coord)
    return data

def predict_one(atm_data: AtmData) -> float | None:

    response = requests.post(
            'http://94.139.242.35/predict-one',
            data=atm_data.model_dump_json().encode('utf8'),
            headers=HEADERS,

        )
    if response.status_code == 200:
        return response.json()
    else:
        print(f'Prediction service adapter. Error while making request: {response.status_code}, {response.text}')
        return None
def calculate_target(x_coord, y_coord, address):

    return 1

if __name__ == "__main__":
    process_main_page()
