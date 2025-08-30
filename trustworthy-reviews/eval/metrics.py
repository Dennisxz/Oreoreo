import pandas as pd, numpy as np
from sklearn.metrics import classification_report, average_precision_score
from pipeline.score import score_one

# to calculate metrics like precision, recall, and F1-score
def evaluate(df):
    y_cols = [c for c in ["ad","irrelevant","rant_no_visit"] if c in df.columns]
    y_true = df[y_cols].to_numpy(int) if y_cols else None
    y_pred = []
    rels = []
    for _, r in df.iterrows():
        res = score_one({"text": r["text"]},
                        {"place_name": r.get("place_name",""), "place_category": r.get("place_category","")})
        y_pred.append([int("No Advertisement" in res["policy_flags"]),
                       int("No Irrelevant Content" in res["policy_flags"]),
                       int("No Rant Without Visit" in res["policy_flags"])])
        rels.append(res["scores"]["relevancy"])
    if y_true is not None:
        print(classification_report(y_true, np.array(y_pred), target_names=["ad","irrelevant","rant_no_visit"]))
    if "is_relevant" in df.columns:
        print("AUPRC(relevancy):", average_precision_score(df["is_relevant"], rels))
