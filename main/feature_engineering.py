import pandas as pd
import spacy
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer
from transformers import pipeline
import os

# Loading the excel into pandas
script_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(script_dir, "Reviews_classified_with_synthetic.csv")
df = pd.read_csv(file_path)

# nlp is Spacy's English NLP pipeline for tokenization, 
# POS (Part-of-Speech) tagging (noun, verb etc.) and sentence segmentation

# sentiment_model is the Hugging Face pipeline that 
# outputs positive or negative sentiment with a confidence score

# sentence_model is a transformer model that converts 
# sentences into dense embeddings capturing semantic meaning
nlp = spacy.load("en_core_web_sm")
sentiment_model = pipeline("sentiment-analysis")
sentence_model = SentenceTransformer('all-MiniLM-L6-v2')

# function that extracts basic features from the text
def extract_features(text):
    doc = nlp(str(text))
    features = {}
    # Basic textual features like length and structure of the review
    features['num_chars'] = len(text)
    features['num_words'] = len(doc)
    features['num_sentences'] = len(list(doc.sents))
    # proportion of words in all caps (often idicates emphasis, shouting or spam)
    features['uppercase_ratio'] = sum(1 for t in doc if t.text.isupper()) / max(len(doc), 1)

    features['num_nouns'] = sum(1 for t in doc if t.pos_ == "NOUN")
    features['num_verbs'] = sum(1 for t in doc if t.pos_ == "VERB")

    # flag if text countains a URL (common in advertising or spam)
    features['contains_url'] = int(any("http" in t.text for t in doc))

    result = sentiment_model(text[:512])[0]  # [:512] to avoid very long input errors
    # binary label for positive or negative sentiment
    features['sentiment_label'] = 1 if result['label'] == "POSITIVE" else 0
    # confidence score of sentiment
    features['sentiment_score'] = result['score']
    # numeric representation later used for mismatch calculation
    features['text_sentiment_value'] = 1 if result['label'] == "POSITIVE" else -1
    return features

# function to map the numeric rating review into a sentiment-like scale, allowing for comparison
# between rating and textual sentiment
def rating_to_sentiment(r):
    if r <= 2:
        return -1
    elif r == 3:
        return 0
    else:
        return 1

# apply feature extractino to the reviews, then concatenate with the original dataframe
text_features = df['text'].apply(extract_features)
text_features_df = pd.DataFrame(list(text_features))
df = pd.concat([df, text_features_df], axis=1)

# TF-IDF is Term Frequency - Inverse Document Frequency
# Term Frequency - how often a word appears in a document
# Inverse Document Frequency - Gives less weight to words that appear in many documents
tfidf = TfidfVectorizer(max_features=100, stop_words='english')
# Convert each review into a vector of numbers representing the importance of each word
tfidf_matrix = tfidf.fit_transform(df['text'])
tfidf_df = pd.DataFrame(tfidf_matrix.toarray(), columns=tfidf.get_feature_names_out())
df = pd.concat([df, tfidf_df], axis=1)

# Sentence embeddings for comparing text and category
# A sentence embedding is a numeric representation of a sentence (or phrase) in a vector space
# Similar sentences will have vectors close to each other in this space.
text_embeddings = sentence_model.encode(df['text'].tolist(), show_progress_bar=True)
category_embeddings = sentence_model.encode(df['rating_category'].tolist(), show_progress_bar=True)
# Compute cosine similarity between each text and its rating category
# Cosine similarity measures how similar two vectors are
similarities = [cosine_similarity([t], [c])[0][0] for t, c in zip(text_embeddings, category_embeddings)]
df['category_similarity'] = similarities

# Sentence embeddings to be processed in the model
embedding_df = pd.DataFrame(text_embeddings, columns=[f'emb_{i}' for i in range(text_embeddings.shape[1])])
df = pd.concat([df, embedding_df], axis=1)

# Compute rating sentiment and mismatch
df['rating_sentiment'] = df['rating'].apply(rating_to_sentiment)
df['sentiment_mismatch'] = (df['text_sentiment_value'] - df['rating_sentiment']).abs()

# Flag potentially irrelevant reviews: mismatch > 1 OR category similarity < threshold
similarity_threshold = 0.3
df['potentially_irrelevant'] = ((df['sentiment_mismatch'] > 1) | (df['category_similarity'] < similarity_threshold)).astype(int)

# export the new csv with all the features
output_path = os.path.join(script_dir, "reviews_with_features.csv")
df.to_csv(output_path, index=False)
print("Feature engineering complete!")