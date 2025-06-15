"""Tests for CLI integration with since logic."""

import datetime
import json
import os
import tempfile
from unittest import mock

import sqlite_utils
from click.testing import CliRunner

from toggl_to_sqlite.cli import cli


def test_cli_automatic_since_detection():
    """Test that CLI uses automatic since detection for incremental updates."""
    runner = CliRunner()

    with tempfile.TemporaryDirectory() as temp_dir:
        # Create auth file
        auth_file = os.path.join(temp_dir, "auth.json")
        with open(auth_file, "w") as f:
            json.dump({"api_token": "test_token"}, f)

        db_file = os.path.join(temp_dir, "test.db")

        # Mock the API calls
        with (
            mock.patch("toggl_to_sqlite.utils.get_workspaces") as mock_workspaces,
            mock.patch("toggl_to_sqlite.utils.get_projects") as mock_projects,
            mock.patch("toggl_to_sqlite.utils.get_time_entries") as mock_time_entries,
            mock.patch("toggl_to_sqlite.utils.get_start_datetime") as mock_start_datetime,
        ):
            mock_workspaces.return_value = [[{"id": 1, "name": "Test Workspace"}]]
            mock_projects.return_value = [[{"id": 1, "name": "Test Project"}]]
            mock_time_entries.return_value = [[{"id": 1, "description": "Test Entry"}]]
            mock_start_datetime.return_value = datetime.date(2023, 1, 1)

            # First run - should use fallback to workspace creation date
            result = runner.invoke(cli, ["fetch", db_file, "--auth", auth_file, "--days", "30", "--type", "time_entries"])

            assert result.exit_code == 0
            assert "📅 Fetching time entries since 2023-01-01" in result.output

            # Verify since table was created
            db = sqlite_utils.Database(db_file)
            assert "time_entries_since" in db.table_names()

            # Second run - should use automatic since detection
            # Reset mocks to verify different call pattern
            mock_time_entries.reset_mock()

            result = runner.invoke(
                cli,
                [
                    "fetch",
                    db_file,
                    "--auth",
                    auth_file,
                    "--days",
                    "30",  # Should be ignored due to automatic since
                    "--type",
                    "time_entries",
                ],
            )

            assert result.exit_code == 0
            assert "📅 Fetching time entries since" in result.output
            assert "days)" in result.output  # Should show calculated days

            # Verify get_time_entries was called with calculated days, not original 30
            mock_time_entries.assert_called_once()
            call_args = mock_time_entries.call_args
            assert call_args[1]["days"] != 30  # Should be calculated days, not original


def test_cli_force_full_sync():
    """Test that --force-full ignores previous sync times."""
    runner = CliRunner()

    with tempfile.TemporaryDirectory() as temp_dir:
        auth_file = os.path.join(temp_dir, "auth.json")
        with open(auth_file, "w") as f:
            json.dump({"api_token": "test_token"}, f)

        db_file = os.path.join(temp_dir, "test.db")

        # Create a database with existing sync time
        db = sqlite_utils.Database(db_file)
        from toggl_to_sqlite.utils import update_sync_time

        past_time = datetime.datetime(2023, 1, 1, 10, 0, 0)
        update_sync_time(db, "time_entries", past_time)

        with mock.patch("toggl_to_sqlite.utils.get_time_entries") as mock_time_entries:
            mock_time_entries.return_value = [[{"id": 1, "description": "Test Entry"}]]

            result = runner.invoke(
                cli, ["fetch", db_file, "--auth", auth_file, "--days", "7", "--force-full", "--type", "time_entries"]
            )

            assert result.exit_code == 0
            assert "Force full sync requested" in result.output
            assert "Fetching time entries for the last 7 days" in result.output

            # Verify get_time_entries was called with original days parameter
            mock_time_entries.assert_called_once()
            call_args = mock_time_entries.call_args
            assert call_args[1]["days"] == 7


def test_cli_user_since_override():
    """Test that user-provided --since overrides automatic detection."""
    runner = CliRunner()

    with tempfile.TemporaryDirectory() as temp_dir:
        auth_file = os.path.join(temp_dir, "auth.json")
        with open(auth_file, "w") as f:
            json.dump({"api_token": "test_token"}, f)

        db_file = os.path.join(temp_dir, "test.db")

        # Create database with existing sync time
        db = sqlite_utils.Database(db_file)
        from toggl_to_sqlite.utils import update_sync_time

        past_time = datetime.datetime(2023, 1, 1, 10, 0, 0)
        update_sync_time(db, "time_entries", past_time)

        with mock.patch("toggl_to_sqlite.utils.get_time_entries") as mock_time_entries:
            mock_time_entries.return_value = [[{"id": 1, "description": "Test Entry"}]]

            user_since = "2023-06-01"
            result = runner.invoke(cli, ["fetch", db_file, "--auth", auth_file, "--since", user_since, "--type", "time_entries"])

            assert result.exit_code == 0
            assert "📅 Fetching time entries since user-specified date: 2023-06-01" in result.output

            # Verify get_time_entries was called with user-provided since
            mock_time_entries.assert_called_once()
            call_args = mock_time_entries.call_args
            assert call_args[1]["since"] is not None


def test_cli_multiple_data_types_sync_tracking():
    """Test that different data types have independent sync tracking."""
    runner = CliRunner()

    with tempfile.TemporaryDirectory() as temp_dir:
        auth_file = os.path.join(temp_dir, "auth.json")
        with open(auth_file, "w") as f:
            json.dump({"api_token": "test_token"}, f)

        db_file = os.path.join(temp_dir, "test.db")

        with (
            mock.patch("toggl_to_sqlite.utils.get_workspaces") as mock_workspaces,
            mock.patch("toggl_to_sqlite.utils.get_projects") as mock_projects,
            mock.patch("toggl_to_sqlite.utils.get_time_entries") as mock_time_entries,
        ):
            mock_workspaces.return_value = [[{"id": 1, "name": "Test Workspace"}]]
            mock_projects.return_value = [[{"id": 1, "name": "Test Project"}]]
            mock_time_entries.return_value = [[{"id": 1, "description": "Test Entry"}]]

            # Fetch all data types
            result = runner.invoke(
                cli,
                [
                    "fetch",
                    db_file,
                    "--auth",
                    auth_file,
                    "--days",
                    "30",
                    "--type",
                    "time_entries",
                    "--type",
                    "workspaces",
                    "--type",
                    "projects",
                ],
            )

            assert result.exit_code == 0

            # Verify separate since tables were created
            db = sqlite_utils.Database(db_file)
            assert "time_entries_since" in db.table_names()
            assert "workspaces_since" in db.table_names()
            assert "projects_since" in db.table_names()

            # Verify all have sync times
            from toggl_to_sqlite.utils import get_last_sync_time

            assert get_last_sync_time(db, "time_entries") is not None
            assert get_last_sync_time(db, "workspaces") is not None
            assert get_last_sync_time(db, "projects") is not None
