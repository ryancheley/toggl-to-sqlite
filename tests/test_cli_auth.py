"""Tests for the CLI auth command."""

import json
import os
import tempfile
from unittest import mock

from click.testing import CliRunner

from toggl_to_sqlite.cli import cli


def test_auth_command_creates_file():
    """Test that auth command creates auth file with API token."""
    runner = CliRunner()

    with tempfile.TemporaryDirectory() as temp_dir:
        auth_file = os.path.join(temp_dir, "test_auth.json")

        # Mock the input function to provide a test API token
        with mock.patch("builtins.input", return_value="test_api_token_12345"):
            result = runner.invoke(cli, ["auth", "--auth", auth_file])

            assert result.exit_code == 0
            assert "Visit this page and sign in with your Toggl account:" in result.output
            assert "https://track.toggl.com/profile" in result.output
            assert f"Authentication tokens written to {auth_file}" in result.output

            # Verify the file was created with correct content
            assert os.path.exists(auth_file)

            with open(auth_file, "r") as f:
                auth_data = json.load(f)

            assert auth_data == {"api_token": "test_api_token_12345"}


def test_auth_command_default_file():
    """Test that auth command uses default auth.json filename."""
    runner = CliRunner()

    with tempfile.TemporaryDirectory() as temp_dir:
        # Change to temp directory so auth.json is created there
        original_cwd = os.getcwd()
        os.chdir(temp_dir)

        try:
            with mock.patch("builtins.input", return_value="default_token"):
                result = runner.invoke(cli, ["auth"])

                assert result.exit_code == 0
                assert "Authentication tokens written to auth.json" in result.output

                # Verify default file was created
                assert os.path.exists("auth.json")

                with open("auth.json", "r") as f:
                    auth_data = json.load(f)

                assert auth_data["api_token"] == "default_token"
        finally:
            os.chdir(original_cwd)


def test_auth_command_overwrites_existing():
    """Test that auth command overwrites existing auth file."""
    runner = CliRunner()

    with tempfile.TemporaryDirectory() as temp_dir:
        auth_file = os.path.join(temp_dir, "existing_auth.json")

        # Create existing auth file
        with open(auth_file, "w") as f:
            json.dump({"api_token": "old_token"}, f)

        # Run auth command with new token
        with mock.patch("builtins.input", return_value="new_token_54321"):
            result = runner.invoke(cli, ["auth", "--auth", auth_file])

            assert result.exit_code == 0

            # Verify file was overwritten
            with open(auth_file, "r") as f:
                auth_data = json.load(f)

            assert auth_data["api_token"] == "new_token_54321"


def test_auth_command_shows_instructions():
    """Test that auth command displays proper user instructions."""
    runner = CliRunner()

    with tempfile.TemporaryDirectory() as temp_dir:
        auth_file = os.path.join(temp_dir, "instructions_test.json")

        with mock.patch("builtins.input", return_value="instruction_token"):
            result = runner.invoke(cli, ["auth", "--auth", auth_file])

            # Check that expected instruction text is present
            output = result.output
            assert "Visit this page and sign in with your Toggl account:" in output
            assert "https://track.toggl.com/profile" in output
            assert f"Authentication tokens written to {auth_file}" in output
