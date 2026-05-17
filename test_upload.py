import os
import sys
import cloudinary
import cloudinary.uploader
from dotenv import load_dotenv

load_dotenv()
try:
    with open("test.txt", "w") as f:
        f.write("test")
    res = cloudinary.uploader.upload("test.txt", resource_type="raw", folder="students")
    print(res.get("secure_url"))
except Exception as e:
    print(f"Error: {e}")
