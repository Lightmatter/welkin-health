"""Package version information."""
from datetime import date
from importlib.metadata import distribution

_dist_metadata: dict = distribution("welkin").metadata.json

__title__ = _dist_metadata["name"]
__description__ = _dist_metadata["summary"]
__url__ = _dist_metadata["home_page"]
__version__ = _dist_metadata["version"]
__author__ = _dist_metadata["author"]
__author_email__ = _dist_metadata["author_email"]
__license__ = _dist_metadata["license"]
__copyright__ = f"{date.today().year} Lightmatter"
