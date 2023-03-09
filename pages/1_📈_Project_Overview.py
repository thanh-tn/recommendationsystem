import streamlit as st
from PIL import Image
import base64

import warnings
warnings.filterwarnings("ignore")



st.set_page_config(page_title="Project Overview", page_icon="📈")




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

image_file = 'files/bg_1.jpg'
background_image(image_file)

st.markdown("# Project Overview")
st.header("I. Project Objectives")
"""
This project aims to provide users of Tiki.vn (a top 2 Vietnamese e-commerce website and top 6 of South East Asian) with a recommender system 
for their product choices.

It deploys two major paradigms of recommender systems : collaborative and content based methods with several Machine Learning packages/ 
algorithms are utilized for similarities checking, like: Gensim, Cosine, ALS and Surprise. 
"""
"\n"
st.header("II. Literature Overview")
"""
Recommender systems are algorithms providing personalized suggestions for items that are most relevant to each user. With the massive growth of 
available online contents, users have been inundated with choices. It is therefore crucial for web platforms to offer recommendations of items to 
each user, in order to increase user satisfaction and engagement.

There are two main types of Recommender System: Content based filtering and Collaborative filtering.
"""
"\n"
image = Image.open('files/recommender system.png')

st.image(image, caption='Two main types of Recommender System')
"\n"
st.subheader("Collaborative Filtering Methods")
"""
Collaborative methods for recommender systems are methods that are based solely on the past interactions recorded between users and items in 
order to produce new recommendations. These interactions are stored in the so-called “user-item interactions matrix”. Collaborative methods use 
these past user-item interactions to detect similar users and/or similar items and make predictions based on these estimated proximities.
"""
"\n"
st.subheader("Content Based Methods")
"""
Unlike collaborative methods that only rely on the user-item interactions, content based approaches use additional information about users and/or 
items. Then, the idea of content based methods is to try to build a model, based on the available “features”, that explain the observed user-item 
interactions.

Source: https://towardsdatascience.com/introduction-to-recommender-systems-6c66cf15ada
"""
"\n"
st.header("III. Project Design")
"""
In this project, I have deployed several packages and algorithms, including: Gensim, Cosine, ALS and Surprise to build a recommender system 
based on data of 4,373 products and 364,099 customer reviews. Below is the comparison across methods:
"""
"\n"
image = Image.open('files/comparison.png')

st.image(image, caption='Comparison across recommender system methods')
"\n"
"""
Regarding Surprise package, Baseline Only was the final algorithm chosen after running several algorithms as below:
"""
"\n"
image = Image.open('files/Surprise.png')

st.image(image, caption='Comparison across Surprise algorithms')
"\n"
st.header("IV. Demo App")
"""
This demo app is built for both Content Based Method and Collaborative Filtering Method.

1. Content Based Method: The package is chosen for demo is Gensim for its superiority in processing time and storage. The app also delivers two 
approaches for users in using Gensim: 
* by choosing product from fixed list and ask system for recommendation
* by inputing product descritions and ask system for recommendation

2. Collaborative Filtering Method: Surprise - Baseline Only is the final package algorithm chosen for demo
"""
"\n"
st.header("V. Author's Recommendations")
"""
Content Based Method and Collaborative Filtering Method are two different approaches and useful for distinct situations. 

However, if we need to choose one over the other, it is recommended to choose Content Based method for below reasons:
* Processing time of content_based is much faster & storage is much lightes, which will not make customers to wait for long and be disappointed 
at processing speed of app
* Number of users who have product ratings is much smaller relative to number of possible reviews based on unique number of customers and products. 
That makes ALS slower in processing, not mention cases that having too big number of customers and products which surely makes processting time of 
ALS even higher and will disappoint customers.
* Collaborative method might not be suitable for new websites or company which has not got customer rating for products.
"""