"""
Basic utilities.
"""
# Authors : Lei Fu <lei.fu.rice@gmail.com>
# License: 

import numpy as np
from typing import Any, Dict, List, Optional, Tuple

__all__ = ['remove_suffix', 'find_all']

def remove_suffix(s: str, suffix: str) -> str:
    """Remove suffix from a string

    Parameters
    ----------
    s : str
        Input string.
    suffix : str
        suffix to be removed
        
    Returns
    -------
    s : str
        String with suffix removed.
    """
    if suffix and s.endswith(suffix):
        return s[:-len(suffix)]
    return s

def find_all(s: str, sub: str, start: int = None, end: int = None) -> List[str]:
    """"Return a list containing all the indexes in s where substring sub is found
        such that sub is contained within s[start:end].  Optional
        arguments start and end are interpreted as in slice notation.
        Return -1 on failure.

    Parameters
    ----------
    s : str
        Input string.
    sub : str
        Substring to find
        
    Returns
    -------
    res : List[str]
        A list with all the indexes in s[start:end] where substring sub is found.
    """

    if s == '' or sub == '':
        return []

    len_s, len_sub = len(s), len(sub)

    if start is None:
        start = 0
    if end is None:
        end = len_s
    elif end < 0:
        end = len_s + end

    res = []

    for i in range(start, end - len_sub + 1):
        if s[i:(i+len_sub)] == sub:
            res.append(i)

    # while start < len(s):
    #     i = s.find(sub, start, end)
    #     print(start, end, i)
    #     if i != -1:
    #         res.append(i)
    #         start = i + 1
    #     else:
    #         break
    return res

if __name__ == "__main__":
    # assert find_all('', '') == []
    # assert find_all(' ', '') == []
    # assert find_all('', ' ') == []
    # assert find_all("a.txt", "t") == [2, 4]
    # assert find_all("a.txt", "t", 2) == [2, 4]
    assert find_all("a.txt", "t", 2, -1) == [2]