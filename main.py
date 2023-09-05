import streamlit as st
import polars as pl
import base64
from datetime import datetime
from utils.database import insert_word, retrieve_words
import plotly.express as px  # Import Plotly

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

    # Convert to Pandas DataFrame for easier manipulation and plotting
    word_frequencies_pd = word_frequencies.to_pandas()

    # Create a Plotly bar chart
    fig = px.bar(word_frequencies_pd, x='word', y='count', title=f'Word Frequencies for {selected_month} {selected_year}')

    # Display the Plotly chart in Streamlit
    st.plotly_chart(fig)

if __name__ == "__main__":
    main()