def Weather():
    # Required Libraries
    import streamlit as st
    import matplotlib.pyplot as plt
    from matplotlib import dates
    from datetime import datetime
    from matplotlib import rcParams
    from pyowm.commons.exceptions import NotFoundError
    import pyowm
    from pyowm.utils.config import get_default_config
    import custom_css as ct

    # Streamlit Display
    # st.set_page_config(layout="centered")
    ct.display_header_page("📅 DỰ BÁO THỜI TIẾT 🌥️ ☔ ")

    col1, mid, col2 = st.columns([80, 5, 140])

    ct.display_header_section("🌐 Nhập tên thành phố và hệ nhiệt độ . Ứng dụng sẽ cho bạn biết thời tiết của 6 ngày tính từ ngày hôm nay", underline=False)
    place = st.text_input("TÊN THÀNH PHỐ (KHÔNG DẤU VÀ THEO CHUẨN QUỐC TẾ, VD: Ha Noi) 🌆 ", "Ha Noi")
    unit = st.selectbox(" CHỌN HỆ NHIỆT ĐỘ 🌡 ", ("Độ C", "Độ F"))
    button = st.button("Dự đoán thời tiết")

    # To deceive error of pyplot global warning

    st.set_option('deprecation.showPyplotGlobalUse', False)

    def plot_line(days, min_t, max_t):
        days = dates.date2num(days)
        rcParams['figure.figsize'] = 6, 4
        plt.plot(days, max_t, color='black', linestyle='solid', linewidth=1, marker='o', markerfacecolor='green',
                markersize=7)
        plt.plot(days, min_t, color='black', linestyle='solid', linewidth=1, marker='o', markerfacecolor='blue',
                markersize=7)
        plt.ylim(min(min_t) - 4, max(max_t) + 4)
        plt.xticks(days)
        x_y_axis = plt.gca()
        xaxis_format = dates.DateFormatter('%d/%m')

        x_y_axis.xaxis.set_major_formatter(xaxis_format)
        plt.grid(True, color='brown')
        plt.legend(["Nhiệt độ cao nhất", "Nhiệt độ thấp nhất"], loc=1)
        plt.xlabel('Ngày(ngày/tháng)')
        plt.ylabel('Nhiệt độ')
        plt.title('Dự báo thời tiết trong 6 ngày')

        for i in range(5):
            plt.text(days[i], min_t[i] - 1.5, min_t[i],
                    horizontalalignment='center',
                    verticalalignment='bottom',
                    color='black')
        for i in range(5):
            plt.text(days[i], max_t[i] + 0.5, max_t[i],
                    horizontalalignment='center',
                    verticalalignment='bottom',
                    color='black')
        # plt.show()
        # plt.savefig('figure_line.png')
        st.pyplot()
        plt.clf()


    def plot_bars(days, min_t, max_t):
        # print(days)
        days = dates.date2num(days)
        rcParams['figure.figsize'] = 6, 4
        min_temp_bar = plt.bar(days - 0.2, min_t, width=0.4, color='r')
        max_temp_bar = plt.bar(days + 0.2, max_t, width=0.4, color='b')
        plt.xticks(days)
        x_y_axis = plt.gca()
        xaxis_format = dates.DateFormatter('%d/%m')

        x_y_axis.xaxis.set_major_formatter(xaxis_format)
        plt.xlabel('Ngày(ngày/tháng)')
        plt.ylabel('Nhiệt độ')
        plt.title('Dự báo thời tiết trong 6 ngày')

        for bar_chart in [min_temp_bar, max_temp_bar]:
            for index, bar in enumerate(bar_chart):
                height = bar.get_height()
                xpos = bar.get_x() + bar.get_width() / 2.0
                ypos = height
                label_text = str(int(height))
                plt.text(xpos, ypos, label_text,
                        horizontalalignment='center',
                        verticalalignment='bottom',
                        color='black')
        st.pyplot()
        plt.clf()


    # Main function
    def weather_detail(place, unit):
        config_dict = get_default_config()
        config_dict['language'] = 'vi'
        owm = pyowm.OWM('13396e2da2b93d0b4b2c526651854212')
        mgr = owm.weather_manager()
        days = []
        dates_2 = []
        min_t = []
        max_t = []
        forecaster = mgr.forecast_at_place(place, '3h')
        forecast = forecaster.forecast
        obs = mgr.weather_at_place(place)
        weather = obs.weather
        temperature = weather.temperature(unit='celsius')['temp']
        if unit == 'Độ C':
            unit_c = 'celsius'
        else:
            unit_c = 'fahrenheit'

        for weather in forecast:
            day = datetime.utcfromtimestamp(weather.reference_time())
            date1 = day.date()
            if date1 not in dates_2:
                dates_2.append(date1)
                min_t.append(None)
                max_t.append(None)
                days.append(date1)
            temperature = weather.temperature(unit_c)['temp']
            if not min_t[-1] or temperature < min_t[-1]:
                min_t[-1] = temperature
            if not max_t[-1] or temperature > max_t[-1]:
                max_t[-1] = temperature

        obs = mgr.weather_at_place(place)
        weather = obs.weather
        ct.display_header_section(f"📍 Thời tiết tại {place[0].upper() + place[1:]} hiện giờ: ")
        # st.title()
        if unit_c == 'celsius':
            st.write(f"## 🌡️ Nhiệt độ: {temperature} °C")
        else:
            st.write(f"## 🌡️  Nhiệt độ: {temperature} F")
        st.write(f"## ☁️ Bầu trời: {weather.detailed_status}")
        st.write(f"## 🌪  Sức gió: {round(weather.wind(unit='km_hour')['speed'])} km/h")
        st.write(f"### ⛅️ Mặt trời mọc :     {weather.sunrise_time(timeformat='iso')} GMT")
        st.write(f"### ☁️ Mặt trời lặng :      {weather.sunset_time(timeformat='iso')} GMT")

        # Expected Temperature Alerts
        ct.display_header_section("❄️Dự đoán trạng thái thời tiết và nhiệt độ: ")
        if forecaster.will_have_fog():
            st.write("### ▶️Khả năng cao xuất hiện sương mù🌁")
        if forecaster.will_have_rain():
            st.write("### ▶️Khả năng cao xuất hiện mưa☔")
        if forecaster.will_have_storm():
            st.write("### ▶️Khả năng cao xuất hiện giông⛈️")
        if forecaster.will_have_snow():
            st.write("### ▶️Khả năng cao sẽ có tuyết❄️")
        if forecaster.will_have_tornado():
            st.write("### ▶️Khả năng cao có vòi rồng🌪️")
        if forecaster.will_have_hurricane():
            st.write("### ▶️Khả năng cao có bão🌀")
        if forecaster.will_have_clear():
            st.write("### ▶️Trời đẹp🌞!!")
        if forecaster.will_have_clouds():
            st.write("### ▶️Trời nhiều mây⛅")

        st.write('                ')
        st.write('                ')


        plot_line(days, min_t, max_t)
        plot_bars(days, min_t, max_t)

        # To give max and min temperature
        i = 0
        st.write(f"# 📆 Dự báo giao động nhiệt độ từ hôm nay tới {days[-1].strftime('%d/%m')} ({unit})")
        for obj in days:
            ta = (obj.strftime("%d/%m"))
            st.write(f'### ➡️ {ta} :\t   ({min_t[i]} - {max_t[i]})')
            i += 1


    if button:
        try:
            weather_detail(place, unit)
        except NotFoundError:
            st.write("Vui lòng nhập đúng tên thành phố theo gợi ý")

