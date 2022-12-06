import streamlit as st
import CarPricePage.Auto_Price_Pred as p1
import WeatherPage.Weather_Predict as p2
import FruitPage.Fruits_Vegetable_Classification as p3
import HandWritingPage.HandWriting as p4
import custom_css as ct
import os

st.set_page_config(
    page_title="Machine Learning Project",
    page_icon=":smiley:",
    layout="wide",
    initial_sidebar_state="expanded",
)

def about_section():
    ct.display_header_section("About Project")
    return """
        <p class="text-color paragraph-text">Đồ án của nhóm bao gồm 4 bài nhỏ:</p>
        <ul class="about-list paragraph-text">
            <li>Dự đoán giá xe cũ</li>
            <li>Dự báo thời tiết</li>
            <li>Nhận diện hình ảnh trái cây</li>
            <li>Nhận diện chữ viết tay</li>
        </ul>
        """

def ourteam_section():
    ct.display_header_section("Our Team")
    return f"""
        <div class="container">
            {card_profile("https://cdn.pixabay.com/photo/2022/02/20/13/57/avatar-7024608_1280.png", "Hua Loc Son", "20110712", "Triển khai bài nhận diện trái cây và chữ viết tay")}
            {card_profile("https://cdn.pixabay.com/photo/2022/02/20/14/01/avatar-7024621__480.png", "Nguyen Minh Chien", "20110712", "Triển khai bài dự đoán giá xe cũ")}
            {card_profile("https://cdn.pixabay.com/photo/2022/02/20/13/59/avatar-7024613__480.png", "Nguyen Hung Khang", "20110712", "Triển khai bài dự báo thời tiết")}
        </div>
    """

def card_profile(link_img, name, mssv, desc=None):
    return f"""
        <div class="card-profile">
            <div>
                <div class="cover-photo">
                    <img src="{link_img}" class="profile">
                </div>
                <div class="profile-name">{name}</div>
                <p class="about">MSSV: {mssv}</p>
                <p class="about">Nhiệm Vụ: {desc}</p>
            </div>
            <div class="social-button">
                <i class="fa-brands fa-facebook"></i>
                <i class="fa-brands fa-instagram"></i>
                <i class="fa-brands fa-youtube"></i>
            </div>
        </div>
    """

ct.add_css()

def Welcome():
    ct.display_header_page("Project Machine Learning")
    st.markdown(about_section(), unsafe_allow_html=True)
    st.markdown(ourteam_section(), unsafe_allow_html=True)

page_names_to_funcs = {
    "Welcome": Welcome,
    "Price Predict": p1.AutoPrice,
    "Weather": p2.Weather,
    "Fruits": p3.run,
    "Hand Writing": p4.run,
}

demo_name = st.sidebar.selectbox("", page_names_to_funcs.keys())
page_names_to_funcs[demo_name]()
