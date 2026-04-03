import pickle
import streamlit as st
import requests

# ------------------ FETCH POSTER ------------------ #
def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US"
    data = requests.get(url)
    data = data.json()
    
    # Handle missing poster safely
    if data.get('poster_path'):
        return "https://image.tmdb.org/t/p/w500/" + data['poster_path']
    else:
        return "https://via.placeholder.com/500x750?text=No+Image"


# ------------------ RECOMMEND FUNCTION ------------------ #
def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    
    distances = sorted(
        list(enumerate(similarity[index])),
        reverse=True,
        key=lambda x: x[1]
    )

    recommended_movie_names = []
    recommended_movie_posters = []

    for i in distances[1:6]:
        movie_id = movies.iloc[i[0]].movie_id
        
        recommended_movie_names.append(movies.iloc[i[0]].title)
        recommended_movie_posters.append(fetch_poster(movie_id))

    return recommended_movie_names, recommended_movie_posters


# ------------------ UI ------------------ #
st.set_page_config(page_title="Movie Recommender", layout="wide")

st.title("🎬 Movie Recommender System")

# ------------------ LOAD FILES ------------------ #
movies = pickle.load(open('movies.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

# ------------------ DROPDOWN ------------------ #
movie_list = movies['title'].values

selected_movie = st.selectbox(
    "Type or select a movie",
    movie_list
)

# ------------------ BUTTON ------------------ #
if st.button('Show Recommendation'):
    names, posters = recommend(selected_movie)

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