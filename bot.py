import pandas as pd
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
import os

# Initialize the SentenceTransformer model for embeddings
model = SentenceTransformer('paraphrase-MiniLM-L6-v2')

# Load CSV file (input file path)
input_csv_path = r'D:\company\jupiter\cleaned_03.csv'  # Update this with the correct absolute path to your cleaned CSV

# Check if the file exists
if not os.path.exists(input_csv_path):
    print(f"File not found: {input_csv_path}")
else:
    # Load the cleaned data CSV
    data = pd.read_csv(input_csv_path)

    # Combine the Topic Title and cleaned explanation into a single corpus
    corpus = data['cleaned_title'] + " " + data['cleaned_explanation']

    # Generate embeddings for the corpus using the SentenceTransformer model
    corpus_embeddings = model.encode(corpus, convert_to_numpy=True)

    # Initialize FAISS index for cosine similarity
    dim = corpus_embeddings.shape[1]  # Get the dimensionality of the embeddings
    index = faiss.IndexFlatL2(dim)  # Use L2 distance (Euclidean distance)
    index.add(corpus_embeddings)  # Add the embeddings to the FAISS index

    # Function to get the most relevant answer using FAISS
   # Function to get the most relevant answer using FAISS
# Function to get the most relevant answer using FAISS
def get_most_relevant_answer(query, index, data):
    # Clean and encode the query
    query_embedding = model.encode([query], convert_to_numpy=True)
    
    # Search the FAISS index for the most similar FAQ
    D, I = index.search(query_embedding, 1)  # Search for the most similar FAQ (top 1 result)
    
    # Get the index of the most similar FAQ
    most_similar_idx = I[0][0]
    
    # Return the relevant FAQ answer and the associated replies
    relevant_answer = data.iloc[most_similar_idx]['cleaned_explanation']
    replies = data.iloc[most_similar_idx]['Replies']  # Assuming 'Replies' contains a list of replies
    
    return relevant_answer, replies

# Function to handle the bot response
def faq_bot():
    print("Welcome to the FAQ Bot! Ask me anything or type 'exit' to quit.")
    
    while True:
        query = input("You: ")
        if query.lower() == 'exit':
            break
        
        # Retrieve the most relevant FAQ answer and replies using FAISS
        relevant_answer, replies = get_most_relevant_answer(query, index, data)
        
        # Combine the replies (if there are multiple) to create a final response
        # Ensure that replies are joined properly and cleaned up
        if isinstance(replies, list):
            # Join replies and remove excessive spaces
            combined_replies = " ".join([reply.strip() for reply in replies])
        else:
            combined_replies = replies.strip() if replies else relevant_answer
        
        # Clean up extra spaces and format the final response
        final_response = " ".join(combined_replies.split())  # Remove extra spaces
        
        # Return the final response
        print(f"Bot: {final_response}")

# Start the bot
faq_bot()
