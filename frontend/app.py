import os

import requests
import streamlit as st

API_URL = os.environ.get("API_URL", "http://localhost:8000")

st.title("Mnemosyne Local")
password = st.sidebar.text_input("Ledger password", type="password")
auth = ("user", password)


def show(resp):
    if resp.ok:
        st.json(resp.json())
    else:
        st.error(f"{resp.status_code}: {resp.json().get('detail', resp.text)}")


tab_add, tab_verify, tab_list = st.tabs(["Record", "Verify", "Ledger"])
with tab_add:
    up = st.file_uploader("File to record", key="add")
    if up and st.button("Record SHA-256"):
        show(requests.post(f"{API_URL}/evidence", files={"file": (up.name, up.getvalue())}, auth=auth, timeout=60))
with tab_verify:
    up = st.file_uploader("File to verify", key="verify")
    if up and st.button("Verify"):
        show(requests.post(f"{API_URL}/verify", files={"file": (up.name, up.getvalue())}, auth=auth, timeout=60))
with tab_list:
    if st.button("Refresh"):
        show(requests.get(f"{API_URL}/evidence", auth=auth, timeout=30))
