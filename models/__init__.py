#!/usr/bin/python3
"""Sets up the package"""

from models.engine.file_storage import FileStorage

# Create an Instance Of File_Storage
storage = FileStorage()

# reload The storage file
storage.reload()
