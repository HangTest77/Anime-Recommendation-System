import pickle
import streamlit as st

with open('style.css') as f:
    st.markdown( f'<style>{f.read()}</style>', unsafe_allow_html=True)


# Streamlit UI
st.header("My Anime Recommendation")
st.header("ヾ(＠⌒▽⌒＠)ﾉ") 


# Load data
animes = pickle.load(open('Sun/anime_list.pkl', 'rb'))
similarity_matrix = pickle.load(open('Sun/similary.pkl', 'rb'))


# anime selection
anime_list = animes['name'].values
selected_anime = st.selectbox(
    "Type or select a anime from the dropdown",
    anime_list
)

# display poster
st.write(f"Selected Anime: {selected_anime}")
selected_anime_row = animes[animes['name'] == selected_anime]
if not selected_anime_row.empty:
    poster_link = selected_anime_row.iloc[0]['URL']
    # Display the poster image next to the anime name
    st.image(poster_link)
else:
    st.warning("Anime not found in the dataset.")




# Function to recommend animes
def recommend(anime, animes, similarity_matrix):
    try:
        
        indexName = animes[animes['name'] == anime].index[0]
        distances = sorted(enumerate(similarity_matrix[indexName]), reverse=True, key=lambda x: x[1])
        recommended_anime_names = []
        recommended_anime_links = []  # Store links with anime names
        recommended_anime_posters = []  # Store poster URLs
        
        

        for i in distances[1:6]:
            anime_name = animes.iloc[i[0]].name
            anime_link = f"https://myanimelist.net/anime/{animes.iloc[i[0]].MAL_ID}"  
            poster_url = animes.iloc[i[0]]['URL']
           
            recommended_anime_names.append(anime_name)
            recommended_anime_links.append(anime_link)
            recommended_anime_posters.append(poster_url)


        return recommended_anime_names, recommended_anime_links, recommended_anime_posters
    except IndexError:
        st.warning("Anime not found in the dataset.")
        return [f"{anime_name}"], [f"{anime_link}"], [f"{poster_url}"]





    

if st.button('Show Recommendations'):

    recommended_anime_names, recommended_anime_links, recommended_anime_poster = recommend(selected_anime, animes, similarity_matrix)
    if recommended_anime_names:
        # Display recommended anime links with names
        for name, link, url in zip(recommended_anime_names, recommended_anime_links, recommended_anime_poster):
            st.write("-------------------------------------------------------------------------")
            st.write(f"[{selected_anime}'s Similar Anime]({link})")
            st.image(url)
    else:
        st.warning("No recommendations found for this anime.")



