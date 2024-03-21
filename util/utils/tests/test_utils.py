"""
General tests for all utils.
"""

# Authors: Andreas Mueller <lei.fu.rice@gmail.com>
# License: 

import os
import re
import sys
import warnings

import numpy as np
import pytest

try:
    thisdir = os.path.dirname(os.path.abspath(__file__))
    sys.path.append(os.path.join(thisdir, '..'))
except:
    sys.path.append('..')

from utils import *

def test_remove_suffix():
    """Test."""
    assert remove_suffix("", "") == ""
    assert remove_suffix(" ", "") == " "
    assert remove_suffix("", " ") == ""
    assert remove_suffix("a.txt", ".txt") == "a"
    assert remove_suffix("a.txt", "txt") == "a."

def test_find_all():
    """Test."""
    assert find_all('', '') == []
    assert find_all(' ', '') == []
    assert find_all('', ' ') == []
    assert find_all("a.txt", "t") == [2, 4]
    assert find_all("a.txt", "t", 2) == [2, 4]
    assert find_all("a.txt", "t", 2, -1) == [2]
    assert find_all("atttt", "tt") == [1, 2, 3]
    assert find_all("atttt", "ttt") == [1, 2]