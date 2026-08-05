import os
import logging

from dotenv import load_dotenv
from flask import (
    Flask,
    jsonify,
    redirect,
    url_for,
    session
)
from authlib.integrations.flask_client import OAuth
from werkzeug.middleware.proxy_fix import ProxyFix

from email_module.oauth.token_store import get_token, save_token

load_dotenv()

# --------------------------------------------------
# Logging Configuration
# --------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

logger = logging.getLogger(__name__)

# --------------------------------------------------
# Flask App
# --------------------------------------------------
app = Flask(__name__)

app.config.update(
    SESSION_COOKIE_SECURE=True,
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE="Lax",
)

app.wsgi_app = ProxyFix(
    app.wsgi_app,
    x_proto=1,
    x_host=1
)

app.secret_key = os.getenv("FLASK_SECRET_KEY")

if not app.secret_key:
    logger.critical("FLASK_SECRET_KEY is missing.")
    raise RuntimeError("FLASK_SECRET_KEY is missing from .env")

# --------------------------------------------------
# OAuth Configuration
# --------------------------------------------------
oauth = OAuth(app)

oauth.register(
    name="google",
    client_id=os.environ["GOOGLE_CLIENT_ID"],
    client_secret=os.environ["GOOGLE_CLIENT_SECRET"],
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
    client_kwargs={
        "scope": "openid email profile https://www.googleapis.com/auth/gmail.compose"
    },
)

logger.info("OAuth server initialized successfully.")

# --------------------------------------------------
# Routes
# --------------------------------------------------
@app.route("/")
def home():
    return redirect(url_for("login"))


@app.route("/login")
def login():

    logger.info("Login request received.")

    # User already authenticated
    if "google_token" in session:

        logger.info("Existing OAuth session found.")

        key = save_token(session["google_token"])

        # Updated to FRONTEND_URL to match your Render Environment Variables
        frontend_url = os.getenv(
            "FRONTEND_URL",
            "http://localhost:8501"
        )

        logger.info("Redirecting using existing session.")

        return redirect(
            f"{frontend_url}/?token={key}"
        )

    logger.info("No existing session. Redirecting to Google.")

    redirect_uri = url_for(
        "authorize",
        _external=True
    )

    return oauth.google.authorize_redirect(
        redirect_uri
    )

@app.route("/logout")
def logout():

    session.clear()

    logger.info("User logged out.")

    # Updated to FRONTEND_URL
    frontend_url = os.getenv(
        "FRONTEND_URL",
        "http://localhost:8501"
    )

    return redirect(frontend_url)


@app.route("/authorize")
def authorize():

    try:

        token = oauth.google.authorize_access_token()
        session["google_token"] = token
        logger.info("Google OAuth authentication successful.")

        key = save_token(token)

        # Updated to FRONTEND_URL
        frontend_url = os.getenv(
            "FRONTEND_URL",
            "http://localhost:8501"
        )

        logger.info("Redirecting authenticated user back to Streamlit.")

        return redirect(
            f"{frontend_url}/?token={key}"
        )

    except Exception:

        logger.exception("OAuth authentication failed.")

        return jsonify(
            {
                "success": False,
                "error": "Authentication failed."
            }
        ), 500


@app.route("/token/<token_id>")
def token(token_id):

    logger.info("Token retrieval requested.")

    token_data = get_token(token_id)

    if token_data is None:

        logger.warning("Invalid or expired token requested.")

        return jsonify(
            {
                "success": False,
                "message": "Invalid or expired token."
            }
        ), 404

    logger.info("Temporary OAuth token exchanged successfully.")

    return jsonify(token_data)


# --------------------------------------------------
# Main
# --------------------------------------------------
if __name__ == "__main__":

    logger.info("Starting OAuth server...")

    app.run(
        host="0.0.0.0",
        port=int(
            os.getenv(
                "OAUTH_PORT",
                5000
            )
        ),
        debug=True,
    )