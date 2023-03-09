import streamlit as st
import pandas as pd
import pickle

import warnings
warnings.filterwarnings("ignore")

############################################################################################

st.set_page_config(page_title="Collaborative Filtering", page_icon="🧕")


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

    

# @st.cache_data
def load_data():
    Product = pd.read_csv("files/Product.csv", encoding="utf8", index_col=0)
    Review = pd.read_csv("files/Review.csv", index_col=0)
    Sur_model = pickle.load(open('files/Sur_model.pkl','rb'))
    result = [Product, Review, Sur_model]
    return result
    
## Load data
Product, Review, Sur_model = load_data()

#def app():
st.title("Collaborative Filtering")
pd.set_option('display.max_colwidth', None) # need this option to make sure cell content is displayed in full
Product['short_name'] = Product['name'].str.split('-').str[0]

df_review_product = pd.merge(left=Review, right=Product, how="left", left_on="product_id", right_on="item_id")

############################################################################################


##### CHECK CUSTOMER SIMILARITIES BY SURPRISE MODEL WITH BASELINE ONLY AND RETURN NAMES & IMAGES OF TOP PRODUCTS WITH HIGHEST ESTIMATED RATING #####
def sursim_check(customer_id,model,n):
    # Get estimate score for list of product ids
    df = Review[['product_id']]
    df['rating'] = df['product_id'].apply(lambda x: model.predict(customer_id, x).est)
    df = df.sort_values(by=['rating'], ascending=False)
    # Drop duplicates, if any
    df = df.drop_duplicates()
    output = df.merge(Product,left_on='product_id', right_on='item_id')
    recommended_names = output['short_name'].values.tolist()
    recommended_images = output['image'].values.tolist()
    return recommended_names, recommended_images

############################################################################################

def get_top_history_product_rating(df,customerID, topn):
    df_user = df[df["customer_id"] ==customerID].sort_values(by='rating', ascending=False).head(topn)
    name_prodcuts = df_user["short_name"]
    images = df_user["image"]
    user_his_dct = {
        "name_prodcuts":name_prodcuts,
        "images":images,
        }
    return user_his_dct

############################################################################################


# Input customer id
col11, col12, col13 = st.columns([4,1,4])
with col11:
    number = st.text_input("Input customer id:").strip()

with col13:
    number_of_recommendation = st.number_input(label="Select number of recommendation products", value=8)
# st.write("Your customer id: ", number)

# Choose maximum number of products that system will recommend
# n = st.number_input(label="Select number of recommendation products", value=8)
button = st.button('Get product recommendation 🔍')



# 'Recommend' button
if button:
    try: 
        ## Check inputed ID
        is_in_list_user = int(number) in Review["customer_id"].unique()
        if is_in_list_user:

            customer_id = int(number)

            ## display top history rating product
            st.write(f":green[Top rated products in the history of customer id:] :blue[**{customer_id}**] ")
            n = 4  ## Grid Width number (number of columns/topproduct)
            user_his_dct = get_top_history_product_rating(df_review_product,customer_id, n)
            images_name__hst_zipped = list(zip(user_his_dct["images"], user_his_dct["name_prodcuts"]))

            groups = []
            for i in range(0, len(images_name__hst_zipped), n):
                groups.append(images_name__hst_zipped[i:i+n])

            for group in groups:
                cols = st.columns(n)
                for i, image_zipped in enumerate(group):
                    # print(image_zipped[0])
                    cols[i].image(image_zipped[0], caption=image_zipped[1])

            ## ====================================================
            st.write(f":orange[Here are the products recommendation for customer id:] :blue[**{customer_id}**] ")
            model = Sur_model
            names, images = sursim_check(customer_id,model,number_of_recommendation)
            names = names[:number_of_recommendation]
            images = images[:number_of_recommendation]

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
        else:
            st.warning("🤖 Sorry!!! The Customer ID you entered does not exist, please try again!⚠️")

    except:
        st.warning("🚨 Wrong input Customer ID, please try again! ⚠️")