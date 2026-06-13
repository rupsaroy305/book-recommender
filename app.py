import streamlit as st
import pickle
import pandas as pd
import numpy as np
import urllib.parse


# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="BookBloom | Recommender",
    page_icon="📚",
    layout="wide"
)


# ---------------- CUSTOM CSS ----------------
st.markdown(
    """
    <style>

    .stApp {
        background: linear-gradient(
            135deg,
            #fff0f6,
            #eef8ff,
            #f7f1ff
        );
    }


    .title {
        text-align:center;
        font-size:55px;
        font-weight:800;
        color:#60448a;
    }


    .subtitle {
        text-align:center;
        color:#75658b;
        font-size:18px;
        margin-bottom:30px;
    }


    .book-card {

        background: rgba(255,255,255,0.7);
        backdrop-filter: blur(15px);

        border-radius:25px;

        padding:18px;

        text-align:center;

        height:430px;

        box-shadow:
        0px 10px 30px rgba(120,90,160,0.18);

        transition:0.3s;
    }


    .book-card:hover {
        transform:translateY(-8px);
    }


    .book-title {

        color:#51356f;

        font-weight:700;

        font-size:15px;

        margin-top:12px;
    }


    .author {

        color:#8b789d;

        font-size:14px;

    }


    div.stButton > button {

        width:100%;

        border-radius:25px;

        background:#c9a7e9;

        color:white;

        font-weight:bold;

        border:none;

    }


    div.stButton > button:hover {

        background:#a97bd4;

    }


    </style>
    """,
    unsafe_allow_html=True
)



# ---------------- LOAD DATA ----------------

@st.cache_data
def load_data():

    pt = pickle.load(open("pivot.pkl","rb"))

    similarity_scores = pickle.load(
        open("similarity.pkl","rb")
    )


    books = pd.read_csv("Books_final.csv", low_memory=False)


    books = books.drop_duplicates(
        "Book-Title"
    )


    book_lookup = books.set_index(
        "Book-Title"
    )[
        ["Book-Author","Image-URL-M"]
    ].to_dict("index")


    return pt, similarity_scores, book_lookup



pt, similarity_scores, book_lookup = load_data()



# ---------------- RECOMMEND ----------------

def recommend(book_name):

    if book_name not in pt.index:
        return []


    index = pt.index.get_loc(book_name)


    similar_items = np.argsort(
        similarity_scores[index]
    )[::-1][1:6]


    data=[]


    for idx in similar_items:

        title = pt.index[idx]


        if title in book_lookup:

            data.append(
                [
                    title,
                    book_lookup[title]["Book-Author"],
                    book_lookup[title]["Image-URL-M"]
                ]
            )


    return data



# ---------------- UI ----------------


st.markdown(
    "<div class='title'>📚 BookBloom</div>",
    unsafe_allow_html=True
)


st.markdown(
    "<div class='subtitle'>Find your next favourite story</div>",
    unsafe_allow_html=True
)



# KEEPING DROPDOWN
book_name = st.selectbox(
    "Choose a book",
    sorted(pt.index.tolist())
)



recommend_clicked = st.button(
    "Recommend Books"
)



# Works with button
if recommend_clicked:

    results = recommend(book_name)


    if results:

        cols = st.columns(5)


        for i in range(len(results)):

            with cols[i]:

                title = results[i][0]

                author = results[i][1]

                image = results[i][2]


                url = (
                    "https://www.goodreads.com/search?q="
                    + urllib.parse.quote(title)
                )


                st.markdown(
                    f"""
                    <div class='book-card'>

                    <a href="{url}" target="_blank">

                    <img src="{image}"
                    width="150"
                    style="border-radius:15px;">

                    </a>


                    <div class='book-title'>
                    📖 {title[:35]}
                    </div>


                    <div class='author'>
                    {author}
                    </div>


                    </div>
                    """,
                    unsafe_allow_html=True
                )
