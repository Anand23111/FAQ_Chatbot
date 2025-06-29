


import streamlit as st
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from googletrans import Translator  # Import googletrans for translation
import json
import os

# FAQ data
faq_data = pd.read_csv(r"D:\company\jupiter\cleaned_03.csv")

# Initialize the vectorizer and transform the FAQ titles
vectorizer = TfidfVectorizer(stop_words='english')
title_vectors = vectorizer.fit_transform(faq_data['Topic Title'])

# Function to search for the most relevant topic
def search_faq(query):
    query_vector = vectorizer.transform([query])
    similarities = cosine_similarity(query_vector, title_vectors)
    best_match_idx = similarities.argmax()  # Get the index of the most similar FAQ
    best_match = faq_data.iloc[best_match_idx]
    return best_match

# Function to load or initialize a history of user queries
def load_query_history():
    if os.path.exists("user_queries.json"):
        with open("user_queries.json", "r") as f:
            return json.load(f)
    else:
        return []

# Function to save the user queries to a history file
def save_query_to_history(query):
    history = load_query_history()
    history.append(query)
    with open("user_queries.json", "w") as f:
        json.dump(history, f)

# Function to translate text using Google Translate
def translate_text(text, target_language='en'):
    translator = Translator()
    translated = translator.translate(text, dest=target_language)
    return translated.text

# Streamlit app
def app():
    # Title of the app
    st.title("FAQ Bot")

    # Language selector for translation
    # target_language = st.selectbox("Select language for translation:", ['en', 'es', 'fr', 'de', 'it', 'hi'])
    target_language = st.selectbox(
    "Select language for translation:",
    [
        'en',  # English
        'hi',  # Hindi
        'bn',  # Bengali
        'ta',  # Tamil
        'te',  # Telugu
        'mr',  # Marathi
        'gu',  # Gujarati
        'kn',  # Kannada
        'ml',  # Malayalam
        'pa',  # Punjabi
        'ur',  # Urdu
        'as',  # Assamese
        'or'   # Odia
    ]
)


    # Create a text box for user input
    query = st.text_input("Ask a question:", "")

    # Load query history for suggesting related queries
    query_history = load_query_history()
    
    # When the user submits the query
    if query:
        # Save the current query to history
        save_query_to_history(query)

        # Translate the query to the target language
        translated_query = translate_text(query, target_language)
        st.write(f"Translated Query ({target_language}): {translated_query}")
        
        # Find the most relevant FAQ
        response = search_faq(query)

        # Translate the response to the target language
        translated_title = translate_text(response['Topic Title'], target_language)
        translated_explanation = translate_text(response['Replies'], target_language)
        
        # Display the most relevant FAQ's title and explanation
        st.subheader(f"Question: {translated_title}")
        st.write(f"Answer: {translated_explanation}")

        # Suggest related queries based on query history
        if query_history:
            st.subheader("Related Queries You Might Like:")

            # Create a list of similar queries
            query_vectors = vectorizer.transform(query_history)
            query_similarity = cosine_similarity(query_vectors, vectorizer.transform([query]))

            # Get the top 5 most similar previous queries
            most_similar_indices = query_similarity.flatten().argsort()[-5:][::-1]
            for idx in most_similar_indices:
                if query_similarity[idx] > 0:  # Only suggest queries with non-zero similarity
                    translated_related_query = translate_text(query_history[idx], target_language)
                    st.write(f"- {translated_related_query}")

    else:
        st.write("Please type a question to get started.")

if __name__ == "__main__":
    app()

