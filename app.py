import streamlit as st
from Pages.main_page import main_page
from Pages.glossary import glossary_page
from Pages.news import news_page
from Pages.about import about_page

# Sidebar Navigation
st.set_page_config(layout="wide")
st.sidebar.title("Navigation")
st.sidebar.markdown("Use the sidebar to navigate the application. You can also hide it by clicking the arrow.")
pages = {
    "Main Page": main_page,
    "Glossary": glossary_page,
    "News": news_page,
    "About": about_page
}

selected_page = st.sidebar.radio("Select a Page", list(pages.keys()))

# Render the selected page
pages[selected_page]()
