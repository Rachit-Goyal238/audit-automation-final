import streamlit as st


DEFAULT_EMAIL_DATA = {
    "result": None,
    "subject": "",
    "to": "",
    "cc": "",
    "filename": "",
    "file_bytes": None,
    "attachments": []
}


def initialize():

    if "email_data" not in st.session_state:

        st.session_state.email_data = DEFAULT_EMAIL_DATA.copy()


def get():

    return st.session_state.email_data


def reset():

    st.session_state.email_data = DEFAULT_EMAIL_DATA.copy()