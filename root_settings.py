import os
import sys
"""
prj_settings is part of the standard project stack.  It provides common objects and services 
 (vs properties which are in config.py)
"""

_root_path = None


def app_root():  # used to find files in the root directory...or it's child directories
    global _root_path
    if not _root_path:
        _root_path = os.path.dirname(os.path.abspath(__file__))
    return _root_path


def dev_data_path():
    aroot = app_root()
    dev_datas = aroot.split('/')[:-2]
    dev_data_root = '/'.join(dev_datas)
    return dev_data_root


def set_python_path_here():
    sys.path.append(os.getcwd())

