"""Tests for the toggl_to_sqlite package initialization."""

import sys
from unittest import mock


def test_version_import_success():
    """Test that __version__ is imported successfully from _version."""
    # Import the package to test version loading
    import toggl_to_sqlite

    # Should have a version string
    assert hasattr(toggl_to_sqlite, "__version__")
    assert isinstance(toggl_to_sqlite.__version__, str)
    assert toggl_to_sqlite.__version__ != "unknown"


def test_version_fallback_to_metadata():
    """Test fallback to importlib.metadata when _version import fails."""
    # Mock the _version import to fail
    with mock.patch.dict(sys.modules, {"toggl_to_sqlite._version": None}):
        with mock.patch("importlib.metadata.version", return_value="1.0.0-fallback"):
            # Force reimport to test fallback
            import importlib

            import toggl_to_sqlite

            importlib.reload(toggl_to_sqlite)

            # Should use metadata fallback
            assert toggl_to_sqlite.__version__ == "1.0.0-fallback"


def test_version_fallback_to_unknown():
    """Test fallback to 'unknown' when both imports fail."""
    # Mock both imports to fail
    with mock.patch.dict(sys.modules, {"toggl_to_sqlite._version": None}):
        with mock.patch("importlib.metadata.version", side_effect=ImportError):
            # Force reimport to test fallback
            import importlib

            import toggl_to_sqlite

            importlib.reload(toggl_to_sqlite)

            # Should fallback to unknown
            assert toggl_to_sqlite.__version__ == "unknown"


def test_all_attribute():
    """Test that __all__ is properly defined."""
    import toggl_to_sqlite

    assert hasattr(toggl_to_sqlite, "__all__")
    assert "__version__" in toggl_to_sqlite.__all__
