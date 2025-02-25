# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from .orjson import *
from .orjson import __version__

def dump(obj, fp, *, default=None, option=None):
    """
    Serialize obj as a JSON formatted stream to fp (a .write()-supporting file-like object).

    Parameters
    ----------
    obj: object
        A Python object to be serialized to JSON.
    fp: file-like object
        A file-like object with a write() method.
    default: Optional[Callable[[Any], Any]]
        A function that will be called for objects that are not serializable.
    option: Optional[int]
        Serialization options.
    """
    if not hasattr(fp, 'write'):
        raise TypeError(f"fp must have write() method, not {type(fp)}")
    fp.write(dumps(obj, default=default, option=option).decode('utf-8'))

def load(fp):
    """
    Deserialize fp (a .read()-supporting file-like object containing a JSON document) to a Python object.

    Parameters
    ----------
    fp: file-like object
        A file-like object with a read() method.

    Returns
    -------
    object
        A Python object corresponding to the deserialized JSON document.
    """
    if not hasattr(fp, 'read'):
        raise TypeError(f"fp must have read() method, not {type(fp)}")
    return loads(fp.read())

__all__ = (
    "__version__",
    "dumps",
    "dump",
    "Fragment",
    "JSONDecodeError",
    "JSONEncodeError",
    "loads",
    "load",
    "OPT_APPEND_NEWLINE",
    "OPT_INDENT_2",
    "OPT_NAIVE_UTC",
    "OPT_NON_STR_KEYS",
    "OPT_OMIT_MICROSECONDS",
    "OPT_PASSTHROUGH_DATACLASS",
    "OPT_PASSTHROUGH_DATETIME",
    "OPT_PASSTHROUGH_SUBCLASS",
    "OPT_SERIALIZE_DATACLASS",
    "OPT_SERIALIZE_NUMPY",
    "OPT_SERIALIZE_UUID",
    "OPT_SORT_KEYS",
    "OPT_STRICT_INTEGER",
    "OPT_UTC_Z",
)
