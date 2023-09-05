import streamlit as st
import polars as pl
import base64
from datetime import datetime  # Import datetime

from utils.database import insert_word, retrieve_words

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

# Main function for Streamlit app
def main():
    st.title("Emotional Landscape")

    # Insert a new word
    word = st.text_input("Enter a word:")
    if st.button("Submit"):
        insert_word(word)

    # Retrieve words
    raw_data = retrieve_words()
    df = pl.DataFrame(raw_data)

    # Convert string to datetime object
    min_date = datetime.strptime("2023-09-01", "%Y-%m-%d")
    max_date = datetime.today()

    # Filter by time range
    time_range = st.slider("Select time range:", min_value=min_date, max_value=max_date, value=(min_date, max_date))
    mask = (df['created_at'] >= time_range[0]) & (df['created_at'] <= time_range[1])
    filtered_df = df.filter(mask)

    # Count word frequencies
    word_frequencies = filtered_df.groupby("word").agg(pl.col("word").count().alias("count"))

    # Generate word cloud (replace this with your word cloud generation code)
    st.write("Word Frequencies:", word_frequencies)

if __name__ == "__main__":
    main()