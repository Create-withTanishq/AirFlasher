from pydantic import BaseModel
from typing import Optional

#response model for firmware upload

class FirmwareUploadResponse(BaseModel):
    firmware_name: str
    firmware_version: str
    firmware_description: Optional[str]
    firmware_target_devices: Optional[str]
    firmware_filename: str
    uploaded_at: str
