import streamlit as st
import pickle
import pandas as pd
import requests
import time
@st.cache_data
def fetch_poster(movie_id):
    try:
        url = "https://api.themoviedb.org/3/movie/{}?api_key=18de053031e1cc2a1bd8687f6ad10ed3&language=en-US".format(movie_id)
        response = requests.get(url)
        data = response.json()
        poster_path = data.get('poster_path')

        if poster_path:
            return "https://image.tmdb.org/t/p/w500/" + poster_path
        else:
            return "https://via.placeholder.com/500x750?text=No+Image"

    except Exception as e:
        print(e)
        return "https://via.placeholder.com/500x750?text=Error"

movies_dict= pickle.load(open('movies_dict.pkl',"rb"))
movies = pd.DataFrame(movies_dict)
similarity= pickle.load(open('similarity.pkl',"rb"))

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]

    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    recommended_movies=[]
    recommended_movies_poster=[]
    for i in movie_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_poster.append(fetch_poster(movie_id))
        time.sleep(0.4)
    return recommended_movies,recommended_movies_poster
st.title('Movie Recommender System')
selected_movie_name = st.selectbox(
    "How would you like to be contacted?",
    movies['title'].values)
if st.button('Recommend'):
    names,posters=recommend(selected_movie_name)

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.text(names[0])
        st.image(posters[0])
    with col2:
        st.text(names[1])
        st.image(posters[1])
    with col3:
        st.text(names[2])
        st.image(posters[2])
    with col4:
        st.text(names[3])
        st.image(posters[3])
    with col5:
        st.text(names[4])
        st.image(posters[4])


