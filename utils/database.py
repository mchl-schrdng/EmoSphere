import streamlit as st
import supabase as sp

# Initialize Supabase client
url = st.secrets["SUPABASE_URL"]
api_key = st.secrets["SUPABASE_API_KEY"]
supabase_client = sp.create_client(url, api_key)

def insert_word(word: str):
    """Insère un nouveau mot dans la table user_emotions."""
    data = {"word": word}
    response = supabase_client.table("user_emotions").insert(data).execute()
    return response

def retrieve_words():
    """Retrieve words from the user_emotions table."""
    response = supabase_client.table("user_emotions").select('*').execute()
    if response.error is None:
        return response.data
    else:
        print(f"Error retrieving data: {response.error}")
        return []