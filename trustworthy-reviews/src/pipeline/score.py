import yaml, joblib, os
from rules.policies import ad_hits, is_no_visit, irrel_hint
from models.embed_relevancy import relevancy_score
from pipeline.place_profile import build_profile

TH = yaml.safe_load(open("configs/thresholds.yaml"))
LABELS = ["ad","irrelevant","rant_no_visit"]

# Lazy-load classifier if trained; keep None otherwise (rules+relevancy still work)
_clf = None
def _get_clf():
    global _clf
    if _clf is None and os.path.exists("models_store/baseline_tfidf.pkl"):
        _clf = joblib.load("models_store/baseline_tfidf.pkl")
    return _clf

def score_one(review: dict, place: dict):
    text = (review.get("text") or "").strip()
    probs = {k: 0.0 for k in LABELS}
    clf = _get_clf()
    if clf:
        p = clf.predict_proba([text])[0]
        probs = dict(zip(LABELS, p))

    reasons = []
    hits = ad_hits(text)
    if hits: reasons.append(f"ad_hits={','.join(hits)}")
    if is_no_visit(text): reasons.append("no_visit_phrase")
    if irrel_hint(text):  reasons.append("irrelevant_hint")

    profile = build_profile(place or {})
    rel = relevancy_score(text, profile)

    flags = []
    if (probs["ad"]>=TH["ad"]) and hits: flags.append("No Advertisement")
    if (probs["rant_no_visit"]>=TH["rant_no_visit"]) or is_no_visit(text): flags.append("No Rant Without Visit")
    if (probs["irrelevant"]>=TH["irrelevant"]) or (rel<TH["relevancy_min"]): flags.append("No Irrelevant Content")

    if ("No Advertisement" in flags) and rel<TH["relevancy_min"]:
        action = "reject"
    elif flags:
        action = "flag"
    else:
        action = "allow"

    return {
        "scores": {**probs, "relevancy": rel},
        "policy_flags": flags,
        "final_action": action,
        "reasons": reasons + [f"relevancy={rel:.2f}"]
    }
