import streamlit as st
from email_module.utils.session import get

def render():
    email = get()

    if email.get("result") is None:
        st.info("Awaiting report generation to display preview.")
        return

    st.components.v1.html(
        email["result"]["html"],
        height=600,
        scrolling=True
    )