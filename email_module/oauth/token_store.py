import threading
import time
import uuid
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

logger = logging.getLogger(__name__)
# Token lifetime (seconds)
TOKEN_TTL = 300  # 5 minutes

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
        logger.info(
        f"Removed {len(expired)} expired OAuth token(s)."
    )


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
        logger.info(
        "Temporary OAuth token stored."
        )
        return key


def get_token(key):
    """
    Retrieve the token once.

    Token expires automatically or is removed after first use.
    """

    with _lock:
        _cleanup()

        data = _tokens.pop(key, None)

        if data is None:
            logger.warning(
                "Invalid or expired OAuth token requested."
            )
            return None
        logger.info(
        "OAuth token successfully retrieved."
        )
        return data["token"]