import streamlit as st
from pipeline.score import score_one

st.title("Trustworthy Location Reviews")
col1, col2 = st.columns(2)
with col1:
    place_name = st.text_input("Place name", "Foo Cafe")
    place_cat  = st.text_input("Category", "Cafe")
with col2:
    review_txt = st.text_area("Review text", "Never been, DM me for 50% off! www.promo.xyz", height=160)

if st.button("Score"):
    res = score_one({"text": review_txt},{"place_name":place_name,"place_category":place_cat})
    st.subheader("Policy Flags"); st.write(res["policy_flags"])
    st.subheader("Scores");       st.json(res["scores"])
    st.subheader("Action");       st.write(res["final_action"])
    st.subheader("Reasons");      st.write(res["reasons"])
