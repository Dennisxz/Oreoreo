# Review Classification and Feature Engineering Pipeline

## Overview
 
This project processes, analyses and classifies online reviews. It combines natural language processing, feature engineering
and machine learning to identify three types of reviews:  
1. Normal - Genuine reviews
2. Advertising - Promotional or marketing content
3. Irrelevant content - Off-topic or vague, unhelpful reviews  

The pipeline includes sentiment analysis, TF-IDF, sentence embeddings, rating-category alignment and Random Forest classification with
synthetic data augmentation.

## Project Structure
```bash
project/
│
├── feature_engineering.py         # Extracts text features, TF-IDF, embeddings, category alignment
├── review_analysis.py             # Trains Random Forest classifier with SMOTE
├── Reviews_classified.xlsx        # Original review dataset
├── Reviews_classified_with_synthetic.csv # Dataset with synthetic advertising reviews
├── reviews_with_features.csv      # Feature-enriched dataset
└── README.md
```

## Dependencies
This project requires the following Python packages:
1. pandas - for data manipulation and CSV/Excel operations
2. spacy - for natural language processing (tokenisation, POS tagging, sentence splitting)
3. scikit-learn - for machine learning models, train/test split, TF-IDF vectorisation and evaluation metrics
4. transformers - for sentiment analysis using Hugging Face pipelines
5. sentence-transformers - for generating sentence embeddings and semantic similarity

Install dependencies using  
```bash
pip install pandas numpy scikit-learn spacy transformers sentence-transformers
python -m spacy download en_core_web_sm
```

## Dataset
The dataset used is the Kaggle dataset. OpenAI was used to create pseudolabels for the classification.

## Synthetic Data Generation
- Added synthetic advertising reviews to improve model performance on rare class
- Templates include promotional content with fake URLs

## Feature Engineering (feature_engineering.py)
1. Text Features
    - Character count, word count, sentence count
    - Uppercase ratio (rant without visit)
    - Number of nouns and verbs
    - Presence of URLs (advertisement)
    - Sentiment analysis (positive/negative) (rant without visit)
2. TF-IDF Features
    - Convert text into numerical vectors reflecting word importance (gives a score to plot )
3. Sentence Embeddings
    - Encodes full sentences into dense vectors
    - Enables semantic similarity computations
    - Used for:
        - Comparing review text with the rating category
        - Feeding into machine learning model
4. Category Similarity
    - Compute cosine similarity between the review text and its rating category
    - Helps detect irrelevant content
    - Low similarity - potential mismatch between review content and category
5. Sentiment Mismatch
    - Converts rating to sentiment (1, 2 -> negative, 3 -> neutral, 4, 5 -> positive)
    - Measures difference between text sentiment and rating sentiment
    - Large mismatch - flag as potentially irrelevant

## Machine Learning Classification
1. Data Preparation
    - Drop non-numeric or non-informative columns
    - Target variable: `Review_Classification`
    - Split dataset - 80% training, 20% testing
2. Model
    - Random Forest Classifier
        - `n_estimators=200` (number of trees)
        - `class_weight='balanced'` (handles class imbalance)
    - Trained on engineered features listed above
3. Evaluation
    - Output precision, recall, F1-score for each class

## Usage
1. Run `feature_engineering.py` to generate `review_with_features.csv`. The important columns are `text`, `rating`, `rating_category`. The file path can be edited in `feature_engineering.py` to use another dataset.
2. Run `review_analysis.py` to train the Random Forest classifier and view evaluation metrics.
3. Use the resulting model for classifying new reviews. Remove the testing split part of `review_analysis.py`, using `X` and `y` as the variables.
