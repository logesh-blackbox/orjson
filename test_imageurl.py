#!/usr/bin/env python3

import sys
import os

# Add the build directory to Python path
sys.path.insert(0, '/home/user/workspace/target/debug')

try:
    import orjson
    
    # Test creating an ImageUrl object
    print("Testing ImageUrl creation...")
    image_url = orjson.ImageUrl("https://httpbin.org/image/jpeg")
    print(f"Created ImageUrl: {image_url}")
    print(f"Type: {type(image_url)}")
    
    # Test serialization
    print("\nTesting serialization...")
    data = {
        "message": "Hello World",
        "image": image_url
    }
    
    result = orjson.dumps(data)
    print(f"Serialized result: {result}")
    
    print("\nImageUrl implementation completed successfully!")
    
except ImportError as e:
    print(f"Import error: {e}")
    print("The module might need to be built first")
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
