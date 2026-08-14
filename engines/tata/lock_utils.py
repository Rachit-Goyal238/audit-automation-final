import fcntl
import os
import time
from contextlib import contextmanager


@contextmanager
def file_lock(lock_file_path, timeout=120):
    """
    A context manager for acquiring an exclusive, non-blocking file lock.
    Retries acquiring the lock for a specified timeout period.

    Args:
        lock_file_path (str): The path to the file to use for locking.
        timeout (int): Maximum time in seconds to wait for the lock.

    Raises:
        TimeoutError: If the lock cannot be acquired within the timeout.
    """
    start_time = time.monotonic()
    lock_file = open(lock_file_path, 'w')
    try:
        while time.monotonic() - start_time < timeout:
            try:
                fcntl.flock(lock_file, fcntl.LOCK_EX | fcntl.LOCK_NB)
                yield  # Lock acquired, yield control to the 'with' block
                return
            except (IOError, BlockingIOError):
                time.sleep(1)  # Wait and retry
        raise TimeoutError(f"Could not acquire lock on {lock_file_path} within {timeout} seconds.")
    finally:
        fcntl.flock(lock_file, fcntl.LOCK_UN)  # Release the lock
        lock_file.close()