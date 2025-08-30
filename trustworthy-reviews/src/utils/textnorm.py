import re, unicodedata
from unidecode import unidecode
import emoji

ZW_RE  = re.compile(r"[\u200B-\u200D\uFEFF]")
MULTI_WS = re.compile(r"\s+")
URL_RE = re.compile(r"(https?://|www\.)", re.I)

# helper functions for normalizing text that are used across the project
def normalize_text(s: str) -> str:
    if not isinstance(s, str): return ""
    s = unidecode(s)
    s = emoji.replace_emoji(s, replace=" ")
    s = ZW_RE.sub("", s)
    s = unicodedata.normalize("NFKC", s)
    s = s.strip()
    s = MULTI_WS.sub(" ", s)
    return s

def has_url(s: str) -> bool:
    return bool(URL_RE.search(s or ""))

def basic_stats(s: str):
    s = s or ""
    return {
        "char_count": len(s),
        "token_count": len(s.split()),
        "upper_ratio": sum(c.isupper() for c in s)/max(1,len(s)),
        "excl_ratio": s.count("!")/max(1,len(s)),
    }