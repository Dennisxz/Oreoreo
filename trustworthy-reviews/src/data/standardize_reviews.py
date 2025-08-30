import pandas as pd, numpy as np, os, sys
from pathlib import Path

RAW_IN  = Path("data/raw/reviews.csv")
OUT_DIR = Path("data/processed"); OUT_DIR.mkdir(parents=True, exist_ok=True)
OUT     = OUT_DIR / "reviews.csv"

# Common header name candidates (case-insensitive)
TEXT_CANDS   = ["text","review","review_text","comment","content","body","desc"]
RATING_CANDS = ["rating","stars","score","review_rating"]
PLACE_CANDS  = ["place_name","restaurant_name","name","business_name","venue"]
PLACEID_CANDS= ["place_id","gmap_id","placeId","id"]
TIME_CANDS   = ["created_at","date","time","timestamp","review_time"]
LANG_CANDS   = ["language","lang"]

def pick(df, cands):
    cols = {c.lower(): c for c in df.columns}
    for k in cands:
        if k.lower() in cols: return cols[k.lower()]
    return None

def coerce01(s):
    # turn yes/true/1 → 1, else 0
    return s.astype(str).str.lower().isin(["1","true","yes","y"]).astype("int32")

# cleans and formats data
def main():
    if not RAW_IN.exists():
        sys.exit(f"Missing {RAW_IN}. Put your CSV there.")

    df = pd.read_csv(RAW_IN)
    # Try to find columns automatically
    text_c   = pick(df, TEXT_CANDS)
    rating_c = pick(df, RATING_CANDS)
    place_c  = pick(df, PLACE_CANDS)
    placeid_c= pick(df, PLACEID_CANDS)
    time_c   = pick(df, TIME_CANDS)
    lang_c   = pick(df, LANG_CANDS)

    if not text_c:
        sys.exit("Could not find a text column. Add one named e.g. 'text' or 'review'.")

    out = pd.DataFrame()
    # lightweight id
    out["review_id"] = (df.index.astype(str) + "|" + df[text_c].astype(str)).map(pd.util.hash_pandas_object).astype("int64")
    out["place_id"]  = df[placeid_c] if placeid_c else None
    out["place_name"]= df[place_c] if place_c else None
    out["place_category"] = None
    out["text"] = df[text_c].astype(str).str.replace(r"\s+", " ", regex=True).str.strip()
    out["rating"] = pd.to_numeric(df[rating_c], errors="coerce") if rating_c else None
    out["language"] = df[lang_c] if lang_c else None
    out["created_at"] = df[time_c] if time_c else None
    out["user_id"] = None
    out["user_review_count"] = None
    out["gps_lat"] = None
    out["gps_lng"] = None

    # If your CSV already has labels, keep them (as 0/1)
    for label in ["ad","irrelevant","rant_no_visit","is_relevant"]:
        if label in df.columns:
            out[label] = coerce01(df[label])

    # Drop empty texts
    before = len(out)
    out = out[out["text"].str.len() > 0]
    print(f"Kept {len(out):,}/{before:,} rows. Columns: {list(out.columns)}")

    out.to_csv(OUT, index=False)
    print(f"Wrote {OUT}")

if __name__ == "__main__":
    main()
