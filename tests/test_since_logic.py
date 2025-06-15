"""Tests for the since table logic functionality."""

import datetime
from unittest import mock

import pytest
import sqlite_utils

from toggl_to_sqlite.utils import (
    get_effective_since_date,
    get_last_sync_time,
    update_sync_time,
)


@pytest.fixture
def test_db():
    """Create an in-memory database for testing."""
    return sqlite_utils.Database(":memory:")


def test_get_last_sync_time_no_table(test_db):
    """Test getting sync time when no since table exists."""
    result = get_last_sync_time(test_db, "time_entries")
    assert result is None


def test_get_last_sync_time_empty_table(test_db):
    """Test getting sync time when since table exists but doesn't have id=1."""
    # Create since table with wrong id (our function looks for id=1)
    test_db["time_entries_since"].insert({"id": 2, "since": "2023-01-01T00:00:00"})

    result = get_last_sync_time(test_db, "time_entries")
    assert result is None


def test_update_and_get_sync_time(test_db):
    """Test updating and retrieving sync time."""
    table_name = "time_entries"
    sync_time = datetime.datetime(2023, 6, 15, 12, 30, 45)

    # Update sync time
    update_sync_time(test_db, table_name, sync_time)

    # Verify it was stored correctly
    result = get_last_sync_time(test_db, table_name)
    assert result == sync_time

    # Verify table structure
    since_table = f"{table_name}_since"
    assert since_table in test_db.table_names()

    row = test_db[since_table].get(1)
    assert row["id"] == 1
    assert row["since"] == sync_time.isoformat()


def test_update_sync_time_replaces_existing(test_db):
    """Test that updating sync time replaces existing entries."""
    table_name = "workspaces"

    # First update
    first_time = datetime.datetime(2023, 1, 1, 10, 0, 0)
    update_sync_time(test_db, table_name, first_time)

    # Second update should replace
    second_time = datetime.datetime(2023, 6, 15, 15, 30, 0)
    update_sync_time(test_db, table_name, second_time)

    # Should only have one row with the latest time
    since_table = f"{table_name}_since"
    rows = list(test_db[since_table].rows)
    assert len(rows) == 1
    assert rows[0]["since"] == second_time.isoformat()

    # Verify retrieval
    result = get_last_sync_time(test_db, table_name)
    assert result == second_time


def test_get_effective_since_date_user_provided(test_db):
    """Test that user-provided since takes priority."""
    table_name = "time_entries"
    api_token = "test_token"

    # Set up existing sync time
    existing_time = datetime.datetime(2023, 1, 1, 10, 0, 0)
    update_sync_time(test_db, table_name, existing_time)

    # User-provided time should take priority
    user_time = datetime.datetime(2023, 6, 1, 12, 0, 0)

    with mock.patch("toggl_to_sqlite.utils.get_start_datetime") as mock_start:
        result = get_effective_since_date(api_token, table_name, test_db, user_time)
        assert result == user_time
        mock_start.assert_not_called()


def test_get_effective_since_date_from_database(test_db):
    """Test using sync time from database when no user input."""
    table_name = "projects"
    api_token = "test_token"

    # Set up existing sync time
    existing_time = datetime.datetime(2023, 3, 15, 14, 30, 0)
    update_sync_time(test_db, table_name, existing_time)

    with mock.patch("toggl_to_sqlite.utils.get_start_datetime") as mock_start:
        result = get_effective_since_date(api_token, table_name, test_db)
        assert result == existing_time
        mock_start.assert_not_called()


def test_get_effective_since_date_fallback_to_workspace(test_db):
    """Test fallback to workspace creation date when no other options."""
    table_name = "time_entries"
    api_token = "test_token"
    workspace_date = datetime.date(2022, 12, 1)

    with mock.patch("toggl_to_sqlite.utils.get_start_datetime", return_value=workspace_date) as mock_start:
        result = get_effective_since_date(api_token, table_name, test_db)
        assert result == workspace_date
        mock_start.assert_called_once_with(api_token)


def test_timezone_handling(test_db):
    """Test that timezone-aware datetimes are handled correctly."""
    table_name = "time_entries"

    # Create timezone-aware datetime
    utc_time = datetime.datetime(2023, 6, 15, 10, 30, 45, tzinfo=datetime.timezone.utc)

    # Store and retrieve
    update_sync_time(test_db, table_name, utc_time)
    result = get_last_sync_time(test_db, table_name)

    # Should preserve the original datetime (ISO format doesn't preserve timezone by default)
    # So we compare the base datetime values
    assert result.replace(tzinfo=None) == utc_time.replace(tzinfo=None)


def test_multiple_tables_independent(test_db):
    """Test that different tables maintain independent sync times."""
    time_entries_time = datetime.datetime(2023, 1, 1, 10, 0, 0)
    workspaces_time = datetime.datetime(2023, 6, 15, 15, 30, 0)

    # Update different tables
    update_sync_time(test_db, "time_entries", time_entries_time)
    update_sync_time(test_db, "workspaces", workspaces_time)

    # Verify they're independent
    assert get_last_sync_time(test_db, "time_entries") == time_entries_time
    assert get_last_sync_time(test_db, "workspaces") == workspaces_time

    # Verify separate tables were created
    assert "time_entries_since" in test_db.table_names()
    assert "workspaces_since" in test_db.table_names()


def test_get_last_sync_time_invalid_since_format(test_db):
    """Test error handling when since table has invalid date format."""
    table_name = "time_entries"
    since_table = f"{table_name}_since"

    # Insert row with invalid date format
    test_db[since_table].insert({"id": 1, "since": "invalid_date_format"})

    # Should return None when date parsing fails
    result = get_last_sync_time(test_db, table_name)
    assert result is None


def test_get_last_sync_time_missing_since_column(test_db):
    """Test error handling when since table doesn't have 'since' column."""
    table_name = "projects"
    since_table = f"{table_name}_since"

    # Insert row without 'since' column
    test_db[since_table].insert({"id": 1, "other_column": "some_value"})

    # Should return None when 'since' key is missing
    result = get_last_sync_time(test_db, table_name)
    assert result is None
