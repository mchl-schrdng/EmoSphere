import streamlit as st
import polars as pl
import base64
from datetime import datetime
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

# Initialize session state
if 'time_range' not in st.session_state:
    initial_min_date = datetime.strptime("2023-09-01", "%Y-%m-%d")
    initial_max_date = datetime.today()
    st.session_state.time_range = (initial_min_date, initial_max_date)

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

    # Use date_input for selecting a date range
    time_range = st.date_input("Select date range:", [datetime(2023, 9, 1).date(), datetime.today().date()])

    # Convert date to string for Polars
    min_date_str = time_range[0].strftime("%Y-%m-%d")
    max_date_str = time_range[1].strftime("%Y-%m-%d")

    # Create a Polars mask for filtering
    mask = (df['created_at'] >= pl.lit(min_date_str)) & (df['created_at'] <= pl.lit(max_date_str))
    filtered_df = df.filter(mask)

    # Count word frequencies
    word_frequencies = filtered_df.group_by("word").agg(pl.col("word").count().alias("count"))

    # Generate word cloud (replace this with your word cloud generation code)
    st.write("Word Frequencies:", word_frequencies)

if __name__ == "__main__":
    main()