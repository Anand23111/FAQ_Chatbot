import pandas as pd
import re
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

# Initialize the lemmatizer
lemmatizer = WordNetLemmatizer()

# Manually define a list of common stopwords for text cleaning
stop_words_manual = [
    'i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', 'your', 'yours', 'yourself', 'yourselves',
    'he', 'him', 'his', 'himself', 'she', 'her', 'hers', 'herself', 'it', 'its', 'itself', 'they', 'them', 'their',
    'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', 'these', 'those', 'am', 'is', 'are',
    'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an',
    'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about',
    'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up',
    'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when',
    'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor',
    'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', 'should', 'now',
    'd', 'll', 'm', 'o', 're', 've', 'y', 'ain', 'aren', 'couldn', 'didn', 'doesn', 'hadn', 'hasn', 'haven', 'isn',
    'ma', 'mightn', 'mustn', 'needn', 'shan', 'shouldn', 'wasn', 'weren', 'won', 'wouldn'
]

# Function to clean text: remove emojis, @content, dates, special characters, stopwords, and lowercase
def clean_text_v2(text):
    # Convert to lowercase
    text = text.lower()

    # Remove emojis (non-ASCII characters)
    text = re.sub(r'[^\x00-\x7F]+', '', text)  # Remove non-ASCII characters

    # Remove @mentions (e.g., @username)
    text = re.sub(r'@[\w]+', '', text)  # Remove @content

    # Remove dates in common formats (e.g., dd-mm-yyyy, yyyy-mm-dd)
    text = re.sub(r'\b\d{1,2}[-/]\d{1,2}[-/]\d{2,4}\b', '', text)  # Matches dates like 12-05-2020
    text = re.sub(r'\b\d{4}[-/]\d{1,2}[-/]\d{1,2}\b', '', text)  # Matches dates like 2020-05-12

    # Remove non-alphanumeric characters (except spaces)
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)

    # Tokenize the text and remove stopwords
    words = text.split()
    text = ' '.join([word for word in words if word not in stop_words_manual])

    return text

# Load CSV file (input file path)
input_csv_path = r'D:\company\jupiter\scraped_02.csv'  # Update this with the correct path to your CSV
data = pd.read_csv(input_csv_path)

# Apply the cleaning function to 'Topic Title' and 'Detailed Explanation' columns
data['cleaned_title'] = data['Topic Title'].apply(clean_text_v2)
data['cleaned_explanation'] = data['Replies'].apply(clean_text_v2)

# Save the cleaned data to a new CSV file (output file path)
output_csv_path = 'cleaned_03.csv'  # Update this with your desired output path
data.to_csv(output_csv_path, index=False)

print(f"Cleaned data has been saved to: {output_csv_path}")
