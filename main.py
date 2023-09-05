import streamlit as st
import base64
from datetime import datetime
from utils.database import insert_word, retrieve_words
import plotly.express as px
import pandas as pd
from utils.sentiment_analysis import get_sentiment

def get_image_base64(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

# Style
st.markdown("""
    <style>
    .centered {
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

# Get the Base64 string of the image
img_base64 = get_image_base64("images/logo.png")

# Display centered logo
st.markdown(f'<p class="centered"><img src="data:image/png;base64,{img_base64}" style="max-width:200px; height:auto;"></p>', unsafe_allow_html=True)

# Display centered title
st.markdown('<h1 class="centered">EmoSphere</h1>', unsafe_allow_html=True)

def main():
    st.subheader('', divider='rainbow')
    st.markdown("""
    Welcome to **EmoSphere**, an app that allows you to explore the emotional landscape based on words submitted by users.
    
    ### How to Use
    1. **Enter a Word**: Type a word that represents your current emotion and hit Enter.
    2. **Select Year**: Use the dropdown to filter the data by a specific year.
    3. **View the Graphs**: The two charts below will update to show the top N word frequencies and sentiment distribution for each month in the selected year.
    """)
    st.subheader('', divider='rainbow')

    # Initialize session state
    if 'entered_word' not in st.session_state:
        st.session_state.entered_word = ""

    # Text input for entering a word (limit to one word and convert to lowercase)
    st.session_state.entered_word = st.text_input("Enter a word (one word only):", value=st.session_state.entered_word, max_chars=20).lower()

    # Check if a word has been entered
    if st.session_state.entered_word:
        if " " in st.session_state.entered_word:
            st.error("Please enter only one word without spaces.")
        else:
            insert_word(st.session_state.entered_word)
            st.session_state.entered_word = ""  # Clear the entered word

    # Retrieve words
    raw_data = retrieve_words()
    df_pd = pd.DataFrame(raw_data)
    df_pd['created_at'] = pd.to_datetime(df_pd['created_at'])

    # Use selectbox for selecting a year
    st.subheader('', divider='rainbow')
    selected_year = st.selectbox("Select Year:", list(range(2020, datetime.now().year + 1)), index=datetime.now().year - 2020)

    # Create a Pandas mask for filtering by year
    mask = df_pd['created_at'].dt.year == selected_year
    filtered_df_pd = df_pd[mask]

    # Count word frequencies
    word_frequencies = filtered_df_pd['word'].value_counts().reset_index()
    word_frequencies.columns = ['word', 'count']

    # Use beta_columns layout for side-by-side graphs
    col1, col2 = st.beta_columns(2)

    with col1:
        # Create a Plotly bar chart for word frequencies
        fig_word_freq = px.bar(
            word_frequencies.head(5),
            x='word',
            y='count',
            title=f'Top 5 Word Frequencies for {selected_year}',
            color='count',
            color_continuous_scale='rainbow'
        )
        fig_word_freq.update_traces(marker_line_width=1.5, opacity=0.7)
        st.plotly_chart(fig_word_freq)

    with col2:
        # Calculate sentiment distribution for each month
        sentiment_data = []
        for month_num in range(1, 13):
            sentiment_scores = [get_sentiment(word) for word in filtered_df_pd['word'] if filtered_df_pd['created_at'].dt.month == month_num]
            sentiment_data.append({
                "Month": month_num,
                "Positive": sentiment_scores.count('Positive'),
                "Negative": sentiment_scores.count('Negative'),
                "Neutral": sentiment_scores.count('Neutral')
            })
        
        # Create a Plotly bar chart for sentiment distribution
        sentiment_df = pd.DataFrame(sentiment_data)
        fig_sentiment_dist = px.bar(
            sentiment_df,
            x='Month',
            y=['Positive', 'Negative', 'Neutral'],
            title=f'Sentiment Distribution for Each Month in {selected_year}',
            labels={'variable': 'Sentiment'},
            color_discrete_map={'Positive': 'green', 'Negative': 'red', 'Neutral': 'gray'}
        )
        st.plotly_chart(fig_sentiment_dist)

if __name__ == "__main__":
    main()