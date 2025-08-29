def build_profile(place: dict) -> str:
    name = (place or {}).get("place_name") or (place or {}).get("name") or ""
    cat  = (place or {}).get("place_category") or (place or {}).get("category") or ""
    bits = []
    if name: bits.append(f"Name: {name}")
    if cat:  bits.append(f"Category: {cat}")
    return ". ".join(bits) or "Local business"