def AutoPrice():
    import streamlit as st
    import pandas as pd
    import numpy as np
    import pickle
    import custom_css as ct
    import requests
    from bs4 import BeautifulSoup

    def fetch_car_image(car_model):
        try:
            url = f"https://unsplash.com/s/photos/{car_model} car"
            req = requests.get(url).text
            scrap = BeautifulSoup(req, 'html.parser')
            elements = scrap.select("img.YVj9w[srcset]")[:4]
            links = []
            for e in elements:
                link = e.attrs['srcset'][:e.attrs['srcset'].find("?")]
                links.append(link)
            ct.display_image(links)
            # calories = scrap.find("div", class_="BNeawe iBp4i AP7Wnd").text
            # return calories
        except Exception as e:
            st.error("Can't able to fetch the Calories")
            print(e)

    ct.display_header_page("🚘 Dự Đoán Giá Xe Đã Qua Sử Dụng")

    filename = './CarPricePage/Auto_Price_Pred_Model'
    model = pickle.load(open(filename, 'rb'))

    with st.sidebar:
        st.subheader('Thông số kỹ thuật xe hơi để dự đoán giá')

    make_model = st.sidebar.selectbox("Model Selection", ("Audi A3", "Audi A1", "Opel Insignia", "Opel Astra", "Opel Corsa", "Renault Clio", "Renault Espace", "Renault Duster"))
    hp_kW = st.sidebar.number_input("Horse Power:",min_value=40, max_value=294, value=120, step=5)
    age = st.sidebar.number_input("Age:",min_value=0, max_value=3, value=0, step=1)
    km = st.sidebar.number_input("km:",min_value=0, max_value=317000, value=10000, step=5000)
    Gears = st.sidebar.number_input("Gears:",min_value=5, max_value=8, value=5, step=1)
    Gearing_Type = st.sidebar.radio("Gearing Type", ("Manual", "Automatic", "Semi-automatic"))

    my_dict = {"make_model":make_model, "hp_kW":hp_kW, "age":age, "km":km, "Gears":Gears, "Gearing_Type":Gearing_Type}
    df = pd.DataFrame.from_dict([my_dict])

    cols = {
        "make_model": "Car Model",
        "hp_kW": "Horse Power",
        "age": "Age",
        "km": "km Traveled",
        "Gears": "Gears",
        "Gearing_Type": "Gearing Type"
    }

    df_show = df.copy()
    df_show.rename(columns = cols, inplace = True)
    st.write("Selected Specs: \n")
    st.table(df_show)

    if st.button("Predict"):
        pred = model.predict(df)
        col1, col2 = st.columns(2)
        col1.info("The estimated value of car price is €")
        col2.info(pred[0].astype(int))
        col1.info("The estimated value of car price is VND")
        col2.info(pred[0].astype(int)*25000)

        car_model = df['make_model'].values[0]
        st.write(car_model)
        fetch_car_image(car_model)

    if st.button("Chart"):
        arr = []
        ages = [i for i in range(3)]
        for i in ages:
            my_dict["age"] = i
            df = pd.DataFrame.from_dict([my_dict])
            pred = model.predict(df)
            arr.append(pred)

        arr = np.array(arr)

        chart_data = pd.DataFrame(
            arr,
            columns=['age'])
        st.line_chart(chart_data)

        arr = []
        hp_kW = [i for i in range(40, 294)]
        for i in hp_kW:
            my_dict["hp_kW"] = i
            df = pd.DataFrame.from_dict([my_dict])
            pred = model.predict(df)
            arr.append(pred)

        arr = np.array(arr)

        chart_data = pd.DataFrame(
            arr,
            columns=['Horse Power'])
        st.line_chart(chart_data)

    st.write("\n\n")
