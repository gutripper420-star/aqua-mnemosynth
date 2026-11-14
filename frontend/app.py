import os

import requests
import streamlit as st

API_URL = os.environ.get("API_URL", "http://localhost:8000")

st.title("Mnemosyne")
username = st.sidebar.text_input("Username", value="admin")
password = st.sidebar.text_input("Password", type="password")
case_id = st.sidebar.text_input("Case ID", value="default")
auth = (username, password)


def show(resp):
    if resp.ok:
        st.json(resp.json())
    else:
        try:
            detail = resp.json().get("detail", resp.text)
        except ValueError:
            detail = resp.text
        st.error(f"{resp.status_code}: {detail}")


tab_add, tab_verify, tab_list, tab_audit, tab_users = st.tabs(
    ["Record", "Verify", "Ledger", "Audit", "Users"]
)
with tab_add:
    up = st.file_uploader("File to record", key="add")
    if up and st.button("Record SHA-256"):
        show(requests.post(f"{API_URL}/evidence", files={"file": (up.name, up.getvalue())},
                           data={"case_id": case_id}, auth=auth, timeout=60))
with tab_verify:
    up = st.file_uploader("File to verify", key="verify")
    if up and st.button("Verify"):
        show(requests.post(f"{API_URL}/verify", files={"file": (up.name, up.getvalue())},
                           data={"case_id": case_id}, auth=auth, timeout=60))
with tab_list:
    if st.button("Refresh"):
        show(requests.get(f"{API_URL}/evidence", params={"case_id": case_id}, auth=auth, timeout=30))
with tab_audit:
    if st.button("Verify chain integrity"):
        show(requests.get(f"{API_URL}/ledger/verify-chain", auth=auth, timeout=30))
    if st.button("Export ledger"):
        show(requests.get(f"{API_URL}/ledger/export", params={"case_id": case_id}, auth=auth, timeout=60))
with tab_users:
    new_name = st.text_input("New username")
    new_pw = st.text_input("New password (12+ chars)", type="password")
    new_role = st.selectbox("Role", ["analyst", "auditor"])
    if st.button("Create user"):
        show(requests.post(f"{API_URL}/users", json={"username": new_name, "password": new_pw,
                                                     "role": new_role}, auth=auth, timeout=30))
