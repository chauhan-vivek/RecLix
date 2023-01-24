import re
import streamlit as st
import pandas as pd
import pickle

import base64
def add_bg_from_local(image_file):
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
add_bg_from_local(r'C:\Users\hp\Desktop\rec-flix\static\bg_img.jpg')

#st.markdown(f"""<style> p {background-image: url(r'/static/bg_img.jpg');}</style> """,unsafe_allow_html=True)

st.title('Movie Recommender System')

all_movies = pickle.load(open(r'C:\Users\hp\Desktop\rec-flix\models\all_movies.pkl','rb'))
all_sim = pickle.load(open(r'C:\Users\hp\Desktop\rec-flix\models\cosine_sim_all.pkl','rb'))
df_all = pd.DataFrame(all_movies)
movies_list = df_all['title'].values
indices=pd.Series(df_all.title)

selected_movie_name = st.selectbox(
    'Select movie to recommend.',
    movies_list)

def recommendations(Title,cosine_sim=all_sim):
    recommended_movies=[]
    movie_idx = df_all[df_all['title'] == Title].index[0]
    score_series=pd.Series(cosine_sim[movie_idx]).sort_values(ascending=False)
    top_10_indexes=list(score_series.iloc[1:11].index)
    
    for i in top_10_indexes:
        recommended_movies.append(list(df_all['title'])[i])
    return recommended_movies



if st.button('Recommend'):
    recommended_movies= recommendations(selected_movie_name)
    st.write(f'You selected {selected_movie_name}')
    st.write(f'Your recommended movies are :')
    for movie in recommended_movies:
        st.write(movie)

