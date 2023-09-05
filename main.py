import streamlit as st
import polars as pl
from database import insert_word, retrieve_words

def main():
    st.title("Emotional Landscape")

    # Insert a new word
    word = st.text_input("Enter a word:")
    if st.button("Submit"):
        insert_word(word)

    # Retrieve words
    raw_data = retrieve_words()
    df = pl.DataFrame(raw_data)

    # Filter by time range
    time_range = st.slider("Select time range:", min_value=pl.lit("2023-09-01").to_datetime(), max_value=pl.lit("today").to_datetime(), value=(pl.lit("2023-09-01").to_datetime(), pl.lit("today").to_datetime()))
    mask = (df['created_at'] >= time_range[0]) & (df['created_at'] <= time_range[1])
    filtered_df = df.filter(mask)

    # Count word frequencies
    word_frequencies = filtered_df.groupby("word").agg(pl.col("word").count().alias("count"))

    # Generate word cloud (replace this with your word cloud generation code)
    st.write("Word Frequencies:", word_frequencies)

if __name__ == "__main__":
    main()