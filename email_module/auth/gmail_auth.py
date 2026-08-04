import os
import requests
import streamlit as st

from google.oauth2.credentials import Credentials

CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
OAUTH_URL = os.getenv("OAUTH_URL", "http://localhost:5000")


class GmailAuthenticator:

    def _create_credentials(self, token):

        credentials = Credentials(
            token=token["access_token"],
            refresh_token=token.get("refresh_token"),
            token_uri="https://oauth2.googleapis.com/token",
            client_id=CLIENT_ID,
            client_secret=CLIENT_SECRET,
            scopes=token["scope"].split(),
        )

        st.session_state["google_credentials"] = credentials

        return credentials

    def _exchange_token(self, token_id):

        try:

            response = requests.get(
                f"{OAUTH_URL}/token/{token_id}",
                timeout=10
            )

            response.raise_for_status()

        except requests.exceptions.Timeout:

            st.error(
                "Authentication server timed out."
            )

            return None

        except requests.exceptions.ConnectionError:

            st.error(
                "Cannot reach authentication server."
            )

            return None

        except requests.exceptions.RequestException:

            return None

        token = response.json()

        return self._create_credentials(token)

    def authenticate(self):

        # Already authenticated during this Streamlit session
        if "google_credentials" in st.session_state:

            return st.session_state["google_credentials"]

        # Returned from OAuth server
        token_id = st.query_params.get("token")

        if token_id:

            credentials = self._exchange_token(token_id)

            if credentials:

                st.query_params.clear()

                st.rerun()

            return None

        # No credentials available
        return None