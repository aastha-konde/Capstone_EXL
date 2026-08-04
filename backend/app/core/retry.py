"""Retry utilities for resilience"""

from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type,
)
import duckdb


def with_retry_duckdb(max_attempts: int = 3):
    """Decorator for DuckDB operations with retry"""
    return retry(
        stop=stop_after_attempt(max_attempts),
        wait=wait_exponential(multiplier=1, min=1, max=10),
        retry=retry_if_exception_type((duckdb.Error, TimeoutError)),
        reraise=True
    )


def with_retry_api(max_attempts: int = 3):
    """Decorator for API calls with retry"""
    from requests.exceptions import RequestException

    return retry(
        stop=stop_after_attempt(max_attempts),
        wait=wait_exponential(multiplier=1, min=1, max=10),
        retry=retry_if_exception_type((RequestException, TimeoutError)),
        reraise=True
    )
