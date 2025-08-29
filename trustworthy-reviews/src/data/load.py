import pandas as pd
from utils.textnorm import normalize_text, has_url, basic_stats

def load_reviews(path="data/processed/reviews.csv"):
    df = pd.read_csv(path)
    df["text"] = df["text"].fillna("").astype(str).map(normalize_text)
    bs = df["text"].map(basic_stats).apply(pd.Series)
    df = pd.concat([df, bs], axis=1)
    df["has_url"] = df["text"].map(has_url)
    return df