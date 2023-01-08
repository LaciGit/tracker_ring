import pkg_resources

__version__ = pkg_resources.get_distribution(__name__).version

from tracker.config.config import SETTINGS
