from . import v2_0, v2_1       # makes subpackages accessible 
from .v2_1 import *            # re-export v2_1 as the default version


__all__ = (list(getattr(v2_1, "__all__", [])))