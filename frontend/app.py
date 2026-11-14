import os

import requests
import streamlit as st

API_URL = os.environ.get("API_URL", "http://127.0.0.1:8000").rstrip("/")
MAX_UPLOAD_BYTES = 10 * 1024 * 1024

st.set_page_config(page_title="Mnemosyne Local", page_icon="🛡️")
st.title("🛡️ Mnemosyne Local")
st.markdown(
    "Record and verify SHA-256 digests locally. Files are read in memory for "
    "hashing and are not retained or inspected."
)

if "ledger_password" not in st.session_state:
    st.session_state.ledger_password = ""

if not st.session_state.ledger_password:
    with st.form("login"):
        password = st.text_input("Local ledger password", type="password")
        submitted = st.form_submit_button("Unlock ledger")

    if submitted:
        try:
            response = requests.get(
                f"{API_URL}/health",
                auth=("mnemosyne", password),
                timeout=5,
            )
            response.raise_for_status()
            st.session_state.ledger_password = password
            st.rerun()
        except requests.RequestException:
            st.error("Could not unlock the local ledger. Check the password and service.")
    st.stop()

auth = ("mnemosyne", st.session_state.ledger_password)
with st.sidebar:
    st.caption("Local ledger session")
    if st.button("Lock ledger"):
        st.session_state.ledger_password = ""
        st.rerun()

tab_upload, tab_verify = st.tabs(["📤 Record evidence", "🔍 Verify a file"])

with tab_upload:
    st.header("Record a document")
    uploaded_file = st.file_uploader("Choose a non-sensitive file (maximum 10 MiB)")

    if st.button("Hash & Record"):
        if uploaded_file is None:
            st.warning("Choose a file first.")
        elif uploaded_file.size > MAX_UPLOAD_BYTES:
            st.error("File exceeds the 10 MiB upload limit.")
        else:
            try:
                response = requests.post(
                    f"{API_URL}/upload",
                    files={"file": (uploaded_file.name, uploaded_file.getvalue())},
                    auth=auth,
                    timeout=30,
                )
                response.raise_for_status()
                record = response.json()
                st.success(f"Recorded as entry {record['record_id']}.")
                st.write(f"Filename: {record['filename']}")
                st.code(record["sha256"], language="text")
                st.caption(
                    "Only the filename, digest, and timestamp are stored. "
                    "A digest does not prove a document's source or truth."
                )
            except requests.RequestException:
                st.error("Could not record the file. Check the local API and ledger.")

with tab_verify:
    st.header("Verify against a recorded digest")
    verification_file = st.file_uploader(
        "Choose the file to verify (maximum 10 MiB)",
        key="verification_file",
    )
    if st.button("Verify file"):
        if verification_file is None:
            st.warning("Choose a file first.")
        elif verification_file.size > MAX_UPLOAD_BYTES:
            st.error("File exceeds the 10 MiB upload limit.")
        else:
            try:
                response = requests.post(
                    f"{API_URL}/verify",
                    files={
                        "file": (
                            verification_file.name,
                            verification_file.getvalue(),
                        )
                    },
                    auth=auth,
                    timeout=30,
                )
                response.raise_for_status()
                result = response.json()
                st.code(result["sha256"], language="text")
                if result["match"]:
                    st.success(
                        f"✅ Digest matches ledger entry {result['record_id']} "
                        f"({result['recorded_filename']})."
                    )
                    st.caption(f"Recorded at: {result['recorded_at']}")
                else:
                    st.error("❌ No ledger record has this file's digest.")
            except requests.RequestException:
                st.error("Could not verify the file. Check the local API and ledger.")
