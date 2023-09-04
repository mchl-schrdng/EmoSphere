import streamlit as st
import supabase

# Initialize Supabase client
url = st.secrets["SUPABASE_URL"]
api_key = st.secrets["SUPABASE_API_KEY"]
supabase_client = supabase.create_client(url, api_key)

def insert_word(word: str):
    """Insert a new word into the user_emotions table."""
    table = "user_emotions"
    data = {"word": word}
    response = supabase_client.table(table).insert(data).execute()
    return response

def retrieve_words(time_range):
    """Retrieve words from the user_emotions table based on a selected time range."""
    table = "user_emotions"
    start_time, end_time = time_range
    query = (
        f"SELECT word FROM {table} WHERE created_at >= '{start_time}' AND created_at <= '{end_time}'"
    )
    response = supabase_client.raw(query).execute()
    return response
