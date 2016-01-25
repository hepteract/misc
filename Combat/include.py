# This module should always be compiled into the beginning
# of attack.pyc.

# Begin imports
from __future__ import division
# End imports

# Begin constants
MASK = 0

_BASE = 1
_MAGIC = 2
_BALLISTICS = 4
_ENEMIES = 8
# End constants

# Cleanup code
if __name__ != "attack": raise ImportError, __name__ + " does not support direct import"
