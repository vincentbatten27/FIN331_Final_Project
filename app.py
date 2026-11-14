"""Landing page. Owner: Product manager (David).

The purchase table and filters moved to pages/4_Explore.py. This page becomes the
landing page with links to the four pages (brief step 5).
"""
import streamlit as st

st.set_page_config(page_title="Insider purchases", layout="wide")
st.title("Do insider purchases predict returns?")
st.page_link("pages/4_Explore.py", label="Explore purchases and CAR", icon=":material/table:")
