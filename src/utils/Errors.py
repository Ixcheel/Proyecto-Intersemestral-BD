import random, time
from sqlalchemy.exc import OperationalError

_RETRYABLE_PGCODES = {"40P01", "40001"}

def is_retryable(exc: Exception) -> bool:
    cause = exc.__cause__ or exc.__context__
    if cause and hasattr(cause, "pgcode"):
        return cause.pgcode in _RETRYABLE_PGCODES

    if isinstance(exc, OperationalError):
        orig = getattr(exc, "orig", None)
        if orig and hasattr(orig, "pgcode"):
            return orig.pgcode in _RETRYABLE_PGCODES

    return False


def with_retry(fn, max_retries: int, base: float):
    for attempt in range(max_retries + 1):
        try:
            return fn()
        except Exception as exc:
            if is_retryable(exc) and attempt < max_retries:
                sleep = base * (2 ** attempt) + random.uniform(0, base)
                time.sleep(sleep)
            else:
                raise