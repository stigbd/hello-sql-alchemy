"""Test repository for nrl_sdk_lib."""

import pytest

from hello_sql_alchemy import main


def test_main() -> None:
    """Should run without raising any exceptions."""
    try:
        main()
    except Exception as e:
        pytest.fail(f"Unexpected exception raised: {e}")
