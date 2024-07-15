import pickle
import streamlit as st
import requests


def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=2484b6eaddf6d47caef4e4056403bf9c&language=en-US".format(movie_id)
    response = requests.get(url)
    data = response.json()
    poster_path = data["poster_path"]
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path 

def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters=[]

    for i in distances[1:6]:
        # fetch the movie poster
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_names.append(movies.iloc[i[0]].title)
        recommended_movie_posters.append(fetch_poster(movie_id))

    return recommended_movie_names,recommended_movie_posters


st.header('Movie Recommender System')
movies = pickle.load(open('movies.pkl','rb'))
similarity = pickle.load(open('similarity.pkl','rb'))

movie_list = movies['title'].values
selected_movie = st.selectbox(
    "Type or select a movie from the dropdown",
    movie_list
)

if st.button("Recommend"):
    names, posters = recommend(selected_movie)
    index = 0
    for i in st.columns(5):
        with i:
            st.text(names[index])
            st.image(posters[index])
            index += 1

