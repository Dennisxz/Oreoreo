import re
RE_URL = re.compile(r"(https?://|www\.)", re.I)
RE_PHONE = re.compile(r"(?:\+?\d[\s\-\.()]?){8,}")
RE_AD = re.compile(r"(promo code|discount|whatsapp|dm for price|limited offer|deal|coupon|affiliate)", re.I)
RE_NO_VISIT = re.compile(r"\b(never been|haven'?t visited|didn'?t go|i didn'?t visit|my friend said|heard it('?s)?)\b", re.I)
RE_IRREL = re.compile(r"\b(crypto|forex|iphone update|vpn|insurance quote)\b", re.I)

def ad_hits(text): 
    t = text or ""; hits=[]
    if RE_URL.search(t): hits.append("url")
    if RE_PHONE.search(t): hits.append("phone")
    if RE_AD.search(t): hits.append("promo_phrase")
    return hits

def is_no_visit(text): return bool(RE_NO_VISIT.search(text or ""))
def irrel_hint(text):  return bool(RE_IRREL.search(text or ""))
