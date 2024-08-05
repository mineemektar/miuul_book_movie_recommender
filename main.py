import streamlit as st
import pandas as pd
from scrape import get_image_from_imdb

st.set_page_config(layout='wide', page_title='Book & Movie Recommender', page_icon='🎥')

@st.cache_data
def get_data():
    recommendations_data = pd.read_excel('data/book_recommendations.xlsx')
    books_data = pd.read_excel('data/books.xlsx')
    book_recommendations_data2 = pd.read_excel('data/book_recommendations2.xlsx')
    book_recommendations_data2[['Book1', 'Book2']] = book_recommendations_data2['Book Pair'].apply(eval).apply(pd.Series)
    movie_recommendations_data = pd.read_excel('data/film_recommendations.xlsx')
    movie_recommendations_data2 = pd.read_excel('data/film_recommendations2.xlsx')
    movie_recommendations_data2[['Film1', 'Film2']] = movie_recommendations_data2['Film Pair'].apply(eval).apply(pd.Series)
    movie_data = pd.read_excel('data/movies.xlsx')
    book_to_film_data = pd.read_excel('data/book_to_film_recommendations.xlsx')
    return recommendations_data, books_data, book_recommendations_data2, movie_recommendations_data, movie_recommendations_data2, movie_data, book_to_film_data

recommendations_data, books_data, book_recommendations_data2, movie_recommendations_data, movie_recommendations_data2, movie_data, book_to_film_data = get_data()


st.title(':blue[Book] & :red[Movie] Recommender 📚🎬')

home_tab, book_tab, book2_tab, movie_tab, movie2_tab, mix_tab, panda_tab = st.tabs(["Homepage", "Book📖", "BFF's💞", "Movie🎥", "Movie Night💜", "Mix", "Nothing🐼"])

# Home tab
with home_tab:
    col1, col2, col3 = st.columns([1, 1, 1])
    col1.subheader("Welcome to BMR!")
    col1.markdown('Welcome to our :blue[book]&:red[movie] recommender website. Here, we help people who can not decide on their next book or what movie to watch but has a specific movie or a book type on their mind. You can choose what you want to do from above pages and we will help you decide.')
    col1.image("https://mlpnk72yciwc.i.optimole.com/cqhiHLc.IIZS~2ef73/w:auto/h:auto/q:75/https://bleedingcool.com/wp-content/uploads/2020/05/Harry-Potter-still.-Credit-Warner-Bros..jpg")

    col2.image("https://m.media-amazon.com/images/M/MV5BMTUyMTQ4NDMzNV5BMl5BanBnXkFtZTcwMTE5MzMzMw@@._V1_.jpg")
    col2.subheader("How does it work?")
    col2.markdown("Our system works using a recommendation algorithm. We take the book/movie you chose and find the most similar book/movie to recommend to you while considering the rating of the book/movie.")

    col3.subheader("How can you use it?")
    col3.markdown("Using our website you can get book and movie recommendations based on your selection. If you do not have anything on mind, you can enjoy the ones recommended to you from the most loved books/movies! Also, if you are planning on doing a movie night with your friend or partner or decide on a mutual book to read with your friend or partner, you both each can select a book/movie and we will recommend to you the one suits the most!")
    col3.image("https://i.pinimg.com/originals/44/7c/8f/447c8f52b8dd00ac7505d9c1f3dc3ebb.gif")

# Book tab
with book_tab:
    st.subheader("*:blue[You can get book recommendations based on your book selection or by random.]*")

    # Create two columns for book selection and random books
    select_col, random_col = st.columns(2)

    with select_col:
        st.subheader("Book Recommendations")
        book_names = recommendations_data['Book Name'].unique()
        selected_book = st.selectbox("Choose a book", options=book_names)
        recommend_button = st.button("Recommend")

    with random_col:
        st.subheader("Random Book Recommendations")
        category = st.selectbox("Choose a category", options=["All"] + books_data['categories'].unique().tolist())
        random_button = st.button("Show Random Books")

    # Create a placeholder for the recommendations to be displayed in the second row
    recommendations_placeholder = st.empty()

    if recommend_button:
        recommendations = recommendations_data.loc[recommendations_data['Book Name'] == selected_book, 'Recommendations'].values[0]
        recommendation_list = recommendations.strip("[]").replace("'", "").split(", ")
        
        with recommendations_placeholder.container():
            st.markdown("### Recommendations based on your selection")
            cols = st.columns(len(recommendation_list)) 
            for idx, recommendation in enumerate(recommendation_list):
                recommended_book = books_data[books_data['Book Name'] == recommendation]
                if not recommended_book.empty:
                    title = recommended_book['Book Name'].values[0]
                    author = recommended_book.authors.values[0]
                    img_url = recommended_book.thumbnail.values[0]

                    with cols[idx]:
                        if pd.notnull(img_url):
                            st.image(img_url, width=150)
                        else:
                            st.image("https://via.placeholder.com/500x500.png?text=G%C3%B6rsel%20Bulunamad%C4%B1", width=150)
                        st.markdown(f"**{title}** by {author}")

    if random_button:
        if category == "All":
            random_books = books_data.iloc[:1000].sample(n=5)
        else:
            random_books = books_data[books_data['categories'] == category].sample(n=5)
        
        with recommendations_placeholder.container():
            st.markdown("### Random Book Recommendations")
            cols = st.columns(5)
            for idx, (index, book) in enumerate(random_books.iterrows()):
                title = book['Book Name']
                author = book['authors']
                img_url = book['thumbnail']
                with cols[idx]:
                    if img_url:
                        st.image(img_url, width=150)
                    else:
                        st.image("https://via.placeholder.com/500x500.png?text=G%C3%B6rsel%20Bulunamad%C4%B1", width=150)
                    st.markdown(f"**{title}** by {author}")

# Double Book tab
with book2_tab:
    st.subheader("*:green[This section is for Book Friends Forever! You can get book recommendations based on the book selection of yours and your friend/partner's.]*")    
    b2_col1, b2_col2, b2_col3 = st.columns([1, 1, 1])

    # Book recommendation system for two selected books
    book_names = book_recommendations_data2['Book1'].unique()
    selected_book1 = b2_col1.selectbox("Choose 1. Book", options=book_names)
    selected_book2 = b2_col2.selectbox("Choose 2. Book", options=book_names)

    recommend_button = b2_col3.button("Recommend Books")
    if recommend_button:
        row = book_recommendations_data2[
            ((book_recommendations_data2['Book1'] == selected_book1) & (book_recommendations_data2['Book2'] == selected_book2)) |
            ((book_recommendations_data2['Book1'] == selected_book2) & (book_recommendations_data2['Book2'] == selected_book1))
        ]
        
        if not row.empty:
            recommendations = row.iloc[0]['Recommendations']
            recommendation_list = recommendations.strip("[]").replace("'", "").split(", ")
            
            st.markdown("### Recommendations")
            cols = st.columns(len(recommendation_list)) 
            for idx, recommendation in enumerate(recommendation_list):
                recommended_book = books_data[books_data['Book Name'] == recommendation]
                if not recommended_book.empty:
                    title = recommended_book['Book Name'].values[0]
                    author = recommended_book.authors.values[0]
                    img_url = recommended_book.thumbnail.values[0]

                    with cols[idx]:  # Place each recommendation in its own column
                        if pd.notnull(img_url):  # Check if img_url is not None or NaN
                            st.image(img_url, width=150)
                        else:
                            st.image("https://via.placeholder.com/500x500.png?text=G%C3%B6rsel%20Bulunamad%C4%B1", width=150)
                        st.markdown(f"**{title}** by {author}")

# Movie tab
with movie_tab:
    st.subheader("*:red[You can get movie recommendations based on your movie selection or by random.]*")

    # Create two columns for movie selection and random movies
    select_col, random_col = st.columns(2)

    with select_col:
        st.subheader("Movie Recommendations")
        movie_names = movie_recommendations_data['Film_title'].unique()
        selected_movie = st.selectbox("Choose a movie", options=movie_names)
        recommend_button = st.button("Recommend Movie")

    with random_col:
        st.subheader("Random Movie Recommendations")
        all_genres = movie_data['Generes'].apply(lambda x: eval(x) if isinstance(x, str) else x).explode().unique()
        genre = st.selectbox("Choose a category", options=["All"] + all_genres.tolist())
        random_button = st.button("Show Random Movies")

    # Create a placeholder for the recommendations to be displayed in the second row
    recommendations_placeholder = st.empty()

    if recommend_button:
        recommendations = movie_recommendations_data.loc[movie_recommendations_data['Film_title'] == selected_movie, 'Recommended Films'].values[0]
        recommendation_list = recommendations.strip("[]").replace("'", "").split(", ")
        
        with recommendations_placeholder.container():
            st.markdown("### Recommendations based on your selection")
            cols = st.columns(len(recommendation_list)) 
            for idx, recommendation in enumerate(recommendation_list):
                recommended_movie = movie_data[movie_data['movie title'] == recommendation]
                if not recommended_movie.empty:
                    title = recommended_movie['movie title'].values[0]
                    path = recommended_movie['path'].values[0]
                    img_url = get_image_from_imdb(path)

                    with cols[idx]:
                        if img_url:
                            st.image(img_url, width=150)
                        else:
                            st.image("https://via.placeholder.com/500x500.png?text=G%C3%B6rsel%20Bulunamad%C4%B1", width=150)
                        st.markdown(f"**{title}**")

    if random_button:
        if genre == "All":
            random_movies = movie_data.sample(n=5)
        else:
            random_movies = movie_data[movie_data['Generes'].apply(lambda x: genre in eval(x))].sample(n=5)
        
        with recommendations_placeholder.container():
            st.markdown("### Random Movie Recommendations")
            cols = st.columns(5)
            for idx, (index, movie) in enumerate(random_movies.iterrows()):
                title = movie['movie title']
                path = movie['path']
                img_url = get_image_from_imdb(path)
                with cols[idx]:
                    if img_url:
                        st.image(img_url, width=150)
                    else:
                        st.image("https://via.placeholder.com/500x500.png?text=G%C3%B6rsel%20Bulunamad%C4%B1", width=150)
                    st.markdown(f"**{title}**")

# Movie 2 tab
with movie2_tab:
    st.markdown("*<h3 style='color: pink;'>You can get movie recommendations based on the movie selection of yours and your friend/partner's.</h3>*", unsafe_allow_html=True)
    m2_col1, m2_col2, m2_col3 = st.columns([1, 1, 1])

    # Movie recommendation system for two selected movies
    movie_names = movie_recommendations_data2['Film1'].unique()
    selected_movie1 = m2_col1.selectbox("Choose 1. Movie", options=movie_names)
    selected_movie2 = m2_col2.selectbox("Choose 2. Movie", options=movie_names)

    recommend_button = m2_col3.button("Recommend Movies")
    if recommend_button:
        row = movie_recommendations_data2[
            ((movie_recommendations_data2['Film1'] == selected_movie1) & (movie_recommendations_data2['Film2'] == selected_movie2)) |
            ((movie_recommendations_data2['Film1'] == selected_movie2) & (movie_recommendations_data2['Film2'] == selected_movie1))
        ]
        
        if not row.empty:
            recommendations = row.iloc[0]['Recommendations']
            recommendation_list = recommendations.strip("[]").replace("'", "").split(", ")
            
            st.markdown("### Recommendations")
            cols = st.columns(len(recommendation_list)) 
            for idx, recommendation in enumerate(recommendation_list):
                recommended_movie = movie_data[movie_data['movie title'] == recommendation]
                if not recommended_movie.empty:
                    title = recommended_movie['movie title'].values[0]
                    path = recommended_movie['path'].values[0]
                    img_url = get_image_from_imdb(path)

                    with cols[idx]:  # Place each recommendation in its own column
                        st.image(img_url, width=150)
                        st.markdown(f"**{title}**")

# Mix tab
with mix_tab:
    st.subheader("*Get movie recommendations based on your book selection.*")

    # Create a column for book selection
    book_names = book_to_film_data['Books'].unique()
    selected_book = st.selectbox("Choose a book", options=book_names)
    recommend_button = st.button("Recommend Moviess")

    # Create a placeholder for the recommendations to be displayed
    recommendations_placeholder = st.empty()

    if recommend_button:
        recommendations = book_to_film_data.loc[book_to_film_data['Books'] == selected_book, 'Recommended Films'].values[0]
        recommendation_list = recommendations.strip("[]").replace("'", "").split(", ")
        
        with recommendations_placeholder.container():
            st.markdown("### Movie Recommendations based on your selected book")
            cols = st.columns(len(recommendation_list)) 
            for idx, recommendation in enumerate(recommendation_list):
                recommended_movie = movie_data[movie_data['movie title'] == recommendation]
                if not recommended_movie.empty:
                    title = recommended_movie['movie title'].values[0]
                    path = recommended_movie['path'].values[0]
                    img_url = get_image_from_imdb(path)

                    with cols[idx]:  # Place each recommendation in its own column
                        if img_url:
                            st.image(img_url, width=150)
                        else:
                            st.image("https://via.placeholder.com/500x500.png?text=G%C3%B6rsel%20Bulunamad%C4%B1", width=150)
                        st.markdown(f"**{title}**")

# Nothing tab
with panda_tab:
    st.header("Resting Time!")
    st.write("We encourage people doing nothing once in a while if they do not want to!")
    st.write("So just enjoy doing nothing with this cute panda! 🐼")
    st.image("https://media.istockphoto.com/id/157278376/tr/foto%C4%9Fraf/giant-panda-resting.jpg?s=612x612&w=0&k=20&c=lLAOXQAWEpyL23BmMGxKu22l8jLP7Br8A5sn_coRwks=")
