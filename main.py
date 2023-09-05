import streamlit as st
import base64
from datetime import datetime
from utils.database import insert_word, retrieve_words
import plotly.express as px
import pandas as pd
from textblob import TextBlob

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

# Initialize session state
if 'entered_word' not in st.session_state:
    st.session_state.entered_word = ""

# Main function for Streamlit app
def main():
    st.title("Emotional Landscape")

    # Introductory text
    st.markdown("""
    ## About this App
    Welcome to **EmoSphere**, an app that allows you to explore the emotional landscape based on words submitted by users.
    """)

    # Text input for entering a word
    st.session_state.entered_word = st.text_input("Enter a word:", value=st.session_state.entered_word)

    # Check if a word has been entered
    if st.session_state.entered_word:
        blob = TextBlob(st.session_state.entered_word)
        sentiment_score = blob.sentiment.polarity
        if sentiment_score > 0:
            sentiment = "Positive"
        elif sentiment_score < 0:
            sentiment = "Negative"
        else:
            sentiment = "Neutral"
        
        insert_word(st.session_state.entered_word, sentiment)
        st.session_state.entered_word = ""

    # Retrieve words
    raw_data = retrieve_words()
    df = pl.DataFrame(raw_data)

    # Use selectbox for selecting a month and year
    months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
    selected_month = st.selectbox("Select Month:", months, index=datetime.now().month - 1)
    selected_year = st.selectbox("Select Year:", list(range(2020, datetime.now().year + 1)), index=datetime.now().year - 2020)

    # Convert month name to month number
    month_number = months.index(selected_month) + 1

    # Create a Polars mask for filtering by month and year
    mask = (df['created_at'].year() == pl.lit(selected_year)) & (df['created_at'].month() == pl.lit(month_number))
    filtered_df = df.filter(mask)

    # Count word frequencies
    word_frequencies = filtered_df.group_by("word").agg(pl.col("word").count().alias("count"))

    # Categorize words as positive or negative (modify based on your list of positive/negative words)
    positive_words = ["happy", "joyful", "excited", "love", "glad"]
    negative_words = ["sad", "angry", "frustrated", "hate", "upset"]
    word_frequencies['sentiment'] = word_frequencies['word'].apply(
        lambda x: 'Positive' if x in positive_words else ('Negative' if x in negative_words else 'Neutral')
    )

    # Create a Plotly bar chart for word frequencies
    fig = px.bar(word_frequencies, x='word', y='count', color='sentiment', title=f'Word Frequencies for {selected_month} {selected_year}')
    st.plotly_chart(fig)

    # Calculate the balance between positive and negative words
    positive_count = word_frequencies[word_frequencies['sentiment'] == 'Positive']['count'].sum()
    negative_count = word_frequencies[word_frequencies['sentiment'] == 'Negative']['count'].sum()
    balance = positive_count - negative_count

    # Create a Plotly bar chart for emotional balance
    balance_data = pd.DataFrame({'Sentiment': ['Positive', 'Negative'], 'Count': [positive_count, negative_count]})
    fig_balance = px.bar(balance_data, x='Sentiment', y='Count', title=f'Emotional Balance for {selected_month} {selected_year}')
    st.plotly_chart(fig_balance)

    # Display the emotional balance
    st.write(f"Emotional balance for {selected_month} {selected_year}: {balance}")

if __name__ == "__main__":
    main()