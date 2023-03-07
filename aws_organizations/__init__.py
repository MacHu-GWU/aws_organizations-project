# -*- coding: utf-8 -*-

"""
AWS Organizations SDK enhancement.
"""


from ._version import __version__

__short_description__ = "AWS Organizations SDK enhancement."
__license__ = "MIT"
__author__ = "Sanhe Hu"
__author_email__ = "husanhe@gmail.com"
__github_username__ = "MacHu-GWU"

try:
    from . import better_boto
    from .org_struct import (
        get_org_structure,
    )
except ImportError:
    pass
