import os
from urllib.parse import quote

import requests
import streamlit as st

API_URL = os.environ.get("API_URL", "http://localhost:8000").rstrip("/")

st.set_page_config(page_title="Evidence Integrity Tool", page_icon="🛡️")
st.title("🛡️ Evidence Integrity Ledger")
st.markdown(
    "Record file names and SHA-256 digests in a local SQLite ledger. "
    "The digest verifies bytes, not the identity or authenticity of the source."
)

tab_upload, tab_verify = st.tabs(["📤 Upload & Hash", "🔍 Verify File"])

with tab_upload:
    st.header("Record New Evidence")
    uploaded_file = st.file_uploader("Choose a file (maximum 10 MiB)")

    if st.button("Generate Hash & Record"):
        if uploaded_file is None:
            st.warning("Please upload a file first.")
        elif uploaded_file.size > 10 * 1024 * 1024:
            st.error("File exceeds the 10 MiB upload limit.")
        else:
            try:
                response = requests.post(
                    f"{API_URL}/upload",
                    files={"file": (uploaded_file.name, uploaded_file.getvalue())},
                    timeout=30,
                )
                response.raise_for_status()
                data = response.json()
                st.success(f"Successfully recorded! Record ID: {data['record_id']}")
                st.code(data["sha256"], language="text")
            except requests.RequestException as exc:
                st.error(f"Could not record evidence: {exc}")

with tab_verify:
    st.header("Verify File Integrity")
    verify_filename = st.text_input("Enter the filename exactly as recorded:")
    provided_hash = st.text_input("Enter the SHA-256 hash to verify:")

    if st.button("Verify Hash"):
        if not verify_filename or not provided_hash:
            st.warning("Please fill out both fields.")
        else:
            try:
                response = requests.get(
                    f"{API_URL}/verify/{quote(verify_filename, safe='')}",
                    params={"provided_hash": provided_hash},
                    timeout=10,
                )
                if response.status_code == 404:
                    st.warning("File not found in the ledger.")
                else:
                    response.raise_for_status()
                    data = response.json()
                    if data["match"]:
                        st.success("✅ MATCH: The hash matches the latest ledger record.")
                    else:
                        st.error("❌ MISMATCH: The provided hash does not match the ledger.")
                    st.json(data)
            except requests.RequestException as exc:
                st.error(f"Could not verify evidence: {exc}")
