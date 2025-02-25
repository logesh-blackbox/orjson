import orjson
import pytest
import tempfile
import os

def test_dump_binary_mode():
    data = {"test": "value", "number": 42}
    with tempfile.NamedTemporaryFile(mode='wb', delete=False) as f:
        orjson.dump(data, f)
        fname = f.name
    
    # Read and verify
    with open(fname, 'rb') as f:
        result = orjson.load(f)
    os.unlink(fname)
    assert result == data

def test_dump_text_mode():
    data = {"test": "value", "number": 42}
    with tempfile.NamedTemporaryFile(mode='w', delete=False, encoding='utf-8') as f:
        orjson.dump(data, f)
        fname = f.name
    
    # Read and verify
    with open(fname, 'r', encoding='utf-8') as f:
        result = orjson.load(f)
    os.unlink(fname)
    assert result == data

def test_dump_invalid_fp():
    with pytest.raises(TypeError, match="fp must be a file-like object"):
        orjson.dump({}, "not a file")
    
    class NoWrite:
        pass
    
    with pytest.raises(TypeError, match="fp must have write() method"):
        orjson.dump({}, NoWrite())

def test_load_invalid_fp():
    with pytest.raises(TypeError, match="fp must be a file-like object"):
        orjson.load("not a file")
    
    class NoRead:
        pass
    
    with pytest.raises(TypeError, match="fp must have read() method"):
        orjson.load(NoRead())

def test_dump_load_large_data():
    # Create a large nested structure
    data = {
        "array": list(range(1000)),
        "nested": {"level1": {"level2": {"level3": list(range(1000))}}}
    }
    
    with tempfile.NamedTemporaryFile(mode='wb', delete=False) as f:
        orjson.dump(data, f)
        fname = f.name
    
    # Read and verify
    with open(fname, 'rb') as f:
        result = orjson.load(f)
    os.unlink(fname)
    assert result == data

def test_load_invalid_json():
    with tempfile.NamedTemporaryFile(mode='w', delete=False, encoding='utf-8') as f:
        f.write("invalid json{")
        fname = f.name
    
    with open(fname, 'r', encoding='utf-8') as f:
        with pytest.raises(orjson.JSONDecodeError):
            orjson.load(f)
    os.unlink(fname)

def test_dump_load_empty():
    data = {}
    with tempfile.NamedTemporaryFile(mode='wb', delete=False) as f:
        orjson.dump(data, f)
        fname = f.name
    
    # Read and verify
    with open(fname, 'rb') as f:
        result = orjson.load(f)
    os.unlink(fname)
    assert result == data

def test_dump_load_unicode():
    data = {"unicode": "测试", "emoji": "🐍"}
    with tempfile.NamedTemporaryFile(mode='wb', delete=False) as f:
        orjson.dump(data, f)
        fname = f.name
    
    # Read and verify
    with open(fname, 'rb') as f:
        result = orjson.load(f)
    os.unlink(fname)
    assert result == data
