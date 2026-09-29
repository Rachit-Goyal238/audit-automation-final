import threading
import time
import uuid
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

logger = logging.getLogger(__name__)

# Token lifetime: 8 hours so it survives a normal working session
TOKEN_TTL = 8 * 60 * 60

_lock = threading.Lock()
_tokens = {}


def _cleanup():
    """Remove expired tokens."""
    now = time.time()

    expired = [
        key
        for key, value in _tokens.items()
        if now - value["created_at"] > TOKEN_TTL
    ]

    for key in expired:
        _tokens.pop(key, None)

    if expired:
        logger.info(f"Removed {len(expired)} expired OAuth token(s).")


def save_token(token):
    """
    Save an OAuth token temporarily.

    Returns:
        UUID string used by Streamlit to retrieve it.
    """

    with _lock:
        _cleanup()

        key = str(uuid.uuid4())

        _tokens[key] = {
            "token": token,
            "created_at": time.time()
        }

        logger.info("Temporary OAuth token stored.")

        return key


def get_token(key):
    """
    Retrieve the token by key.

    The token is NOT deleted on retrieval so that page reloads
    can re-authenticate using the same token_id kept in the URL.
    Tokens expire automatically after TOKEN_TTL seconds.
    """

    with _lock:
        _cleanup()

        data = _tokens.get(key, None)   # get(), not pop() — keep it alive

        if data is None:
            logger.warning("Invalid or expired OAuth token requested.")
            return None

        logger.info("OAuth token successfully retrieved.")

        return data["token"]


def delete_token(key):
    """
    Explicitly remove a token. Call this on logout so the
    token_id in the URL can no longer be used to re-authenticate.
    """
    with _lock:
        removed = _tokens.pop(key, None)
        if removed:
            logger.info("OAuth token deleted on logout.")


def update_token(key, token):
    """
    Overwrite the stored token data for an existing key.

    Call this after an access_token refresh so the store stays in sync
    with the live credentials object. If the key no longer exists
    (expired or deleted) this is a no-op.
    """
    with _lock:
        if key in _tokens:
            _tokens[key]["token"] = token
            logger.info("OAuth token updated after refresh.")