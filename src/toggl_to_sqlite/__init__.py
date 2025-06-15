try:
    from ._version import __version__
except ImportError:
    # fallback for development
    try:
        from importlib.metadata import version

        __version__ = version("toggl-to-sqlite")
    except ImportError:
        __version__ = "unknown"

__all__ = ["__version__"]
