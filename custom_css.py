import streamlit as st

def add_css():
  link_faw = """
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.2.1/css/all.min.css" integrity="sha512-MV7K8+y+gLIBoVD59lQIYicR65iaqukzvf/nwasF0nqhPay5w/9lJmVM2hMDcnK1OnMGCdVK+iQrJ7lzPJQd1w==" crossorigin="anonymous" referrerpolicy="no-referrer" />
"""
  st.markdown(link_faw, unsafe_allow_html=True)
  with open('styles.css') as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

def display_header_page(para):
  st.markdown(f"<h2 class='center-header header-page'>{para}</h2>", unsafe_allow_html=True)

def display_header_section(para, underline=True):
  if underline:
    st.markdown(f"<h3 class='header-section header-active'>{para}</h3>", unsafe_allow_html=True)
  else:
    st.markdown(f"<h3 class='header-section'>{para}</h3>", unsafe_allow_html=True)