import streamlit as st
import base64
from datetime import datetime
from utils.database import insert_word, retrieve_words
import plotly.express as px
import pandas as pd  # Import Pandas

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
    2. **Select Month and Year**: Use the dropdowns to filter the data by a specific month and year.
    3. **View the Graph**: The bar chart below will update to show the frequency of each word for the selected time period.
    """)
    st.subheader('', divider='rainbow')
    # Initialize session state
    if 'entered_word' not in st.session_state:
        st.session_state.entered_word = ""

    # Text input for entering a word
    st.session_state.entered_word = st.text_input("Enter a word:", value=st.session_state.entered_word)

    # Check if a word has been entered
    if st.session_state.entered_word:
        insert_word(st.session_state.entered_word)
        st.session_state.entered_word = ""  # Clear the entered word

    # Retrieve words
    raw_data = retrieve_words()
    df_pd = pd.DataFrame(raw_data)
    df_pd['created_at'] = pd.to_datetime(df_pd['created_at'])

    # Use selectbox for selecting a month and year
    st.subheader('', divider='rainbow')
    months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
    selected_month = st.selectbox("Select Month:", months, index=datetime.now().month - 1)
    selected_year = st.selectbox("Select Year:", list(range(2020, datetime.now().year + 1)), index=datetime.now().year - 2020)

    # Convert month name to month number
    month_number = months.index(selected_month) + 1

    # Create a Pandas mask for filtering by month and year
    mask = (df_pd['created_at'].dt.month == month_number) & (df_pd['created_at'].dt.year == selected_year)
    filtered_df_pd = df_pd[mask]

    # Count word frequencies
    word_frequencies = filtered_df_pd['word'].value_counts().reset_index()
    word_frequencies.columns = ['word', 'count']

    # Create a Plotly bar chart
    fig = px.bar(
        word_frequencies,
        x='word',
        y='count',
        title=f'Word Frequencies for {selected_month} {selected_year}',
        color='count',  # Use 'count' column for coloring bars
        color_continuous_scale='viridis',  # Set gradient color scale
    )
    fig.update_traces(marker_line_width=1.5, opacity=0.7)

    # Display the Plotly chart in Streamlit
    st.plotly_chart(fig)

if __name__ == "__main__":
    main()