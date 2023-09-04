import streamlit as st
import supabase

# Initialize Supabase client
url = st.secrets["SUPABASE_URL"]
api_key = st.secrets["SUPABASE_API_KEY"]
supabase_client = supabase.create_client(url, api_key)

def insert_word(word: str):
    # Insert word into the 'words' table
    supabase.table('user_emotions').insert({"word": word}).execute()
