import sys
import os

print(f"Executable: {sys.executable}")
print(f"CWD: {os.getcwd()}")
print("Sys Path:")
for p in sys.path:
    print(f"  - {p}")

try:
    import celery
    print(f"Celery imported from: {celery.__file__}")
except ImportError as e:
    print(f"Failed to import celery: {e}")

try:
    import uvicorn
    print(f"Uvicorn imported from: {uvicorn.__file__}")
except ImportError as e:
    print(f"Failed to import uvicorn: {e}")
