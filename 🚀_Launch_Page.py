import streamlit as st
import base64
import pandas as pd
from underthesea import word_tokenize, pos_tag
from gensim import corpora, models, similarities
#from multiapp import MultiPage
# from pages import P1_Project_Overview, P2_Content_Based_Filtering, P3_Collaborative_Filtering
import warnings
warnings.filterwarnings("ignore")


# Set page layout
st.set_page_config(
    page_title="Recommender system for Tiki.vn",
    page_icon="🛒",
    # layout="wide",
    initial_sidebar_state="expanded",
)



# Set background image
def background_image(image_file):
    with open(image_file, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
    st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url(data:image/{"png"};base64,{encoded_string.decode()});
        background-size: cover
    }}
    </style>
    """,
    unsafe_allow_html=True
    )

image_file = 'files/bg_2.jpg'
background_image(image_file)

# st.markdown("# Recommender system for Tiki.vn 🛒")

st.write("# Welcome to Recommender system for Tiki.vn👋")

st.sidebar.success("Select function above ⬆️")

st.image("files/tikis-scaled.jpg")

st.markdown(
    """
    
"""
)