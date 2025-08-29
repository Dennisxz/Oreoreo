from sentence_transformers import SentenceTransformer, util
_model = None

def get_model():
    global _model
    if _model is None:
        _model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
    return _model

def relevancy_score(review_text: str, place_profile: str) -> float:
    m = get_model()
    emb = m.encode([review_text or "", place_profile or ""], normalize_embeddings=True)
    return float(util.cos_sim(emb[0], emb[1]).item())
