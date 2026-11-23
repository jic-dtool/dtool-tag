"""dtool_tag package."""

from importlib.metadata import version, PackageNotFoundError

try:
    __version__ = version("dtool-tag")
except PackageNotFoundError:
    # Package is not installed.
    __version__ = "unknown"
