import os
from datetime import datetime
from fastapi import UploadFile
from typing import Tuple

UPLOAD_DIR = "backend/static/firmware"

async def save_firmware_file(firmware_file: UploadFile) -> Tuple[str, str]:
    """
    Saves the uploaded firmware file with a timestamped filename.

    Returns:
        new_filename (str): The saved file name
        uploaded_at (str): The timestamp in YYYYMMDD_HHMMSS format
    """
    os.makedirs(UPLOAD_DIR, exist_ok=True)

    # Generate timestamp
    uploaded_at = datetime.now().strftime("%Y%m%d_%H%M%S")
    new_filename = f"{uploaded_at}_{firmware_file.filename}"
    file_path = os.path.join(UPLOAD_DIR, new_filename)

    # Save file
    with open(file_path, "wb") as f:
        f.write(await firmware_file.read())

    return new_filename, uploaded_at
