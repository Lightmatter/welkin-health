"""Package version information."""

from __future__ import annotations

from datetime import datetime, timezone
from importlib.metadata import distribution
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from importlib.metadata._adapters import Message

_metadata: Message = distribution("welkin").metadata

__title__ = _metadata.get("Name")
__description__ = _metadata.get("Summary")
__url__ = _metadata.get("Home-page")
__version__ = _metadata.get("Version")
__author__ = _metadata.get("Author")
__author_email__ = _metadata.get("Author-email")
__license__ = _metadata.get("License")
__copyright__ = f"{datetime.now(tz=timezone.utc):%Y} Lightmatter"
