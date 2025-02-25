# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from .orjson import *
from .orjson import __version__

def dump(obj, fp, /, **kwargs):
    """
    Serialize obj as a JSON formatted stream to fp (a .write()-supporting file-like object).

    Args:
        obj: The Python object to serialize.
        fp: A .write()-supporting file-like object.
        **kwargs: Additional keyword arguments passed to orjson.dumps.

    Raises:
        JSONEncodeError: If obj cannot be serialized to JSON.
    """
    result = dumps(obj, **kwargs)
    if isinstance(fp, (str, bytes)):
        raise TypeError(f"fp must be a file-like object with write() method, not {type(fp).__name__}")
    try:
        if hasattr(fp, 'mode') and 'b' not in fp.mode:
            fp.write(result.decode('utf-8'))
        else:
            fp.write(result)
    except AttributeError:
        raise TypeError(f"fp must have write() method")
    except Exception as e:
        raise TypeError(f"fp.write() failed: {str(e)}")

def load(fp, /):
    """
    Deserialize fp (a .read()-supporting file-like object containing a JSON document) to a Python object.

    Args:
        fp: A .read()-supporting file-like object containing a JSON document.

    Returns:
        The Python object deserialized from the JSON document.

    Raises:
        JSONDecodeError: If the JSON document is invalid.
    """
    if isinstance(fp, (str, bytes)):
        raise TypeError(f"fp must be a file-like object with read() method, not {type(fp).__name__}")
    try:
        content = fp.read()
        if isinstance(content, str):
            content = content.encode('utf-8')
        return loads(content)
    except AttributeError:
        raise TypeError(f"fp must have read() method")
    except Exception as e:
        if isinstance(e, JSONDecodeError):
            raise
        raise TypeError(f"fp.read() failed: {str(e)}")

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
