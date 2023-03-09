import streamlit as st
import pandas as pd
from underthesea import word_tokenize, pos_tag
from gensim import corpora, models, similarities
import base64
import warnings
warnings.filterwarnings("ignore")

from st_clickable_images import clickable_images
# from st_click_detector import click_detector



############################################################################################

st.set_page_config(page_title="Content Based Filtering", page_icon="🔍")



# # Set background image
# def background_image(image_file):
#     with open(image_file, "rb") as image_file:
#         encoded_string = base64.b64encode(image_file.read())
#     st.markdown(
#     f"""
#     <style>
#     .stApp {{
#         background-image: url(data:image/{"png"};base64,{encoded_string.decode()});
#         background-size: cover
#     }}
#     </style>
#     """,
#     unsafe_allow_html=True
#     )

# image_file = 'files/bg_1.jpg'
# background_image(image_file)

st.markdown(
                """
                <style>
                img {
                    cursor: pointer;
                    transition: all .2s ease-in-out;
                }
                img:hover {
                    transform: scale(1.1);
                }
                </style>
                """,
                unsafe_allow_html=True,
            )


#def load data:


@st.cache_data
def load_data():
    Product = pd.read_csv("files/Product.csv", encoding="utf8", index_col=0)
    dictionary = corpora.dictionary.Dictionary.load("files/dictionary.dictionary")
    tfidf = models.tfidfmodel.TfidfModel.load("files/tfidf.tfidfmodel")
    index = similarities.docsim.SparseMatrixSimilarity.load("files/index.docsim")
    result = [Product, dictionary, tfidf, index]
    return result

## Load data
Product, dictionary, tfidf, index = load_data()



st.title("Content Based Filtering")


# Product = pd.read_csv('files/Product.csv', encoding="utf8", index_col=0)
pd.set_option('display.max_colwidth', None) # need this option to make sure cell content is displayed in full
Product['short_name'] = Product['name'].str.split('-').str[0]
product_map = Product.iloc[:,[0,-1]]
product_list = product_map['short_name'].values


############################################################################################

# Define functions to use for both methods
##### TEXT PROCESSING #####
def process_text(document):
    # Change to lower text
    document = document.lower()
    # Remove line break
    document = document.replace(r'[\r\n]+', ' ')
    # Change / by white space
    document = document.replace('/', ' ') 
    # Change , by white space
    document = document.replace(',', ' ') 
    # Remove punctuations
    document = document.replace('[^\w\s]', '')
    punctuation = '!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~'
    for char in punctuation:
        document = document.replace(char, '')
    # Remove numbers, keep words
    document = document.replace('[\w]*\d+[\w]*', '')
    document = document.replace('[0-9]+', '')   
    # Replace mutiple spaces by single space
    document = document.replace('[\s]{2,}', ' ')
    # Word_tokenize
    document = word_tokenize(document, format="text")   
    # Pos_tag
    document = pos_tag(document)    
    # Remove stopwords
    STOP_WORD_FILE = 'files/vietnamese-stopwords.txt'   
    with open(STOP_WORD_FILE, 'r', encoding='utf-8') as file:
        stop_words = file.read()
    stop_words = stop_words.split()  
    document = [[word[0] for word in document if not word[0] in stop_words]] 
    return document

##### TAKE URL OF AN IMAGE #####
def fetch_image(idx):
    selected_product = Product[['image', 'name', 'brand','price', 'group']].iloc[[idx]].reset_index(drop=True) 
    url = selected_product["image"][0]
    name = selected_product["name"][0]
    brand = selected_product["brand"][0]
    price = selected_product["price"][0]
    group = selected_product["group"][0]
    result = {
        "url": url, 
        "name":name,
        "brand": brand,
        "price": price,
        "group": group}
    return result

##### CHECK PRODUCT SIMILARITIES BY GENSIM MODEL AND RETURN NAMES & IMAGES OF TOP PRODUCTS WITH HIGHEST SIMILARITY INDEX #####
def gensim_check(document, dictionary, tfidf, index, n):
    # Convert document to lower text
    document = document.lower().split()
    # Convert document to dictionary according to reference
    vector = dictionary.doc2bow(document)
    # Index similarities of document versus reference
    sim = index[tfidf[vector]]
    # Print output
    list_id = []
    list_score = []
    for i in range(len(sim)):
        list_id.append(i)
        list_score.append(sim[i])
    # Create dataframe to store output
    result = pd.DataFrame({'id':list_id, 'score':list_score})
    # Extract number of products according to users' input (as we choose product from list, extract n+1 items, including the 1st chosen one):
    n_highest_score = result.sort_values(by='score', ascending=False).head(n+1)
    # Extract product_id of above request
    id_tolist = list(n_highest_score['id'])
    recommended_names = []
    recommended_images = []
    for i in id_tolist:
        # Fetch the product names
        product_name = Product['name'].iloc[[i]]
        recommended_names.append(product_name.to_string(index=False))
        # Fetch the product images
        recommended_images.append(fetch_image(i)["url"])
    return recommended_names, recommended_images

############################################################################################

# Define separate page to demo each method
##### CONTENT_BASED FILTERING BY FIXED LIST #####
def filter_list():
    # Markdown name of Content_based method
    st.markdown("### By Fixed List")



    # Fetch image of selected product
    selected_idx = st.selectbox("Select product to view: ", range(len(product_list)), format_func=lambda x: product_list[x])
    idx = selected_idx

    col11, col12 = st.columns([2, 3])
    with col11:
        # Select product from list

        st.image(fetch_image(idx)["url"])
    with col12:
        st.write(f'* **Product name**: {fetch_image(idx)["name"]}')
        st.write(f'* **Brand**: {fetch_image(idx)["brand"]}')
        st.write(f'* **Group**: {fetch_image(idx)["group"]}')
        st.write(f'* **Price**: {fetch_image(idx)["price"]}')

  
    # Choose maximum number of products that system will recommend
    n = st.number_input(label="Select number of recommendation products", value=8)
    button = st.button('Get product recommendation 🔍')
    # 'Recommend' button
    if button:
        st.write("Here are the products recommendation: ")
        selection = Product.iloc[[idx]]
        selection_str = selection['desc'].to_string(index=False)
        document = selection_str
        names, images = gensim_check(document, dictionary, tfidf, index, n+1)
        names = names[1:-1]
        images = images[1:-1]
        images_name_zipped = list(zip(images, names))
       
        n = 4  ## Grid Width number (number of columns)
        groups = []
        for i in range(0, len(images_name_zipped), n):
            groups.append(images_name_zipped[i:i+n])

        for group in groups:
            cols = st.columns(n)
            for i, image_zipped in enumerate(group):
                # print(image_zipped[0])
                cols[i].image(image_zipped[0], caption=image_zipped[1])

    
##### CONTENT_BASED FILTERING BY INPUTING DESCRIPTION #####
def input_description():
    # Markdown name of Content_based method
    st.markdown("### By Inputing Description")

    # input product description
    text_input = st.text_input(
        "Input product description to search: "
    )

    # Choose maximum number of products that system will recommend
    n = st.number_input(label="Select number of recommendation products", value=8)
    button = st.button('Get product recommendation 🔍')
    # 'Recommend' button
    if button:
        document = ' '.join(map(str,process_text(text_input)))
        st.write("Here are the products recommendation: ")
        names, images = gensim_check(document, dictionary, tfidf, index, n+1)
        names = names[:n]
        images = images[:n]

        images_name_zipped = list(zip(images, names))
       
        n = 4  ## Grid Width number (number of columns)
        groups = []
        for i in range(0, len(images_name_zipped), n):
            groups.append(images_name_zipped[i:i+n])

        for group in groups:
            cols = st.columns(n)
            for i, image_zipped in enumerate(group):
                cols[i].image(image_zipped[0], caption=image_zipped[1])


    ##### CALLING PAGE  #####
page_names_to_funcs = {
    "Filter List": filter_list,
    "Input Description": input_description
    }
selected_page = st.sidebar.selectbox("Select method", page_names_to_funcs.keys())
page_names_to_funcs[selected_page]()