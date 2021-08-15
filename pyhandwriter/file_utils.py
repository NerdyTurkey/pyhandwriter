# -*- coding: utf-8 -*-
"""
Created on Tue Oct  6 10:44:23 2020

@author: jt
"""

# For consistency, when in other scripts
# import file_utils as fu
# fu.make_read_only(filename)


import os
import pathlib
import json
import pickle
from stat import S_IREAD, S_IWUSR  # for converting files to readonly/writeable
import subprocess

from .enums import Flag

# ==============================================================================


def file_exists(fname_with_path):
    path = pathlib.Path(fname_with_path)
    return path.exists() and path.is_file()


# ==============================================================================


def get_filenames_with_prefix(prefix, path=None):
    path = path or "."
    return [fname for fname in os.listdir(path) if fname.startswith(prefix)]


# ==============================================================================


def make_read_only(fname):
    """ Makes fname read only """
    try:
        os.chmod(fname, S_IREAD)
    except FileNotFoundError:
        pass
        # print('FileNotFoundError: in file_utils, make_read_only()')


# ==============================================================================


def make_writeable(fname):
    """ Makes fname writeable """
    try:
        os.chmod(fname, S_IWUSR | S_IREAD)
    except FileNotFoundError:
        pass
        # print('FileNotFoundError: in file_utils, make_writeable()')


# ==============================================================================


def hide_file(fname):
    try:
        subprocess.check_call(["attrib", "+H", fname])
    except FileNotFoundError:
        pass
        # print('FileNotFoundError: in file_utils, hide_file()')


# ==============================================================================


def unhide_file(fname):
    try:
        subprocess.check_call(["attrib", "-H", fname])
    except FileNotFoundError:
        pass
        # print('FileNotFoundError: in file_utils, unhide_file()')


# ==============================================================================


def json_dump(data, fname):
    """
    json dump data to file fname.
    Return True if successful else False
    """
    try:
        with open(fname, "w") as f:
            json.dump(data, f)
        return True
    except IOError:
        print("IOError json dumping ", fname)
        return False


# ==============================================================================


def json_load(fname):
    """
    Return data loaded from json file fname.
    If load failed, return fail flag (Enum)
    """
    try:
        with open(fname, "r") as f:
            return json.load(f)
    except IOError:
        print("IOError json loading ", fname)
        return Flag.FAIL  # can't use None since file content might be None


# ==============================================================================


def pickle_dump(data, fname):
    """
    Pickle dump data to file fname.
    Return True if successful else False.
    """
    try:
        with open(fname, "wb") as f:
            pickle.dump(data, f)
        return True
    except IOError:
        print("IOError pickle dumping ", fname)
        return False


# ==============================================================================


def pickle_load(fname):
    """
    Return data pickled-loaded from file fname.
    If load failed, return fail flag (Enum)

    """
    try:
        with open(fname, "rb") as f:
            data = pickle.load(f)
        return data
    except:
        print("IOEror pickle loading ", fname)  # debug
        return Flag.FAIL


# ==============================================================================


def change_extension(fname, ext):
    """
    Change extension of filename fname to ext.
    If fname has no extension, add ext anyway.
    NB: assumes final '.' in fname marks start of extension.
    """
    # add '.' to start of ext if not there already
    if not ext.startswith("."):
        ext = "." + ext

    parts = fname.split(".")
    if len(parts) == 1:
        return parts[0] + ext
    else:
        return ".".join(parts[:-1]) + ext


# ==============================================================================


def add_prefix_to_filename(path, prefix):
    fname = path.split("/")[-1]
    if fname == path:
        return prefix + fname
    else:
        path_without_filename = path[: -len(fname)]
        return path_without_filename + prefix + fname


# =============================================================================


def no_path(fname):
    """
    return just last part of fname, i.e. no path
    """
    return fname.split("/")[-1]


# =============================================================================
