from pydantic import BaseModel
from typing import Optional
import sqlalchemy.orm

#response model for firmware upload

class FirmwareUploadResponse(BaseModel):
    firmware_name: str
    firmware_version: str
    firmware_description: Optional[str]
    firmware_target_devices: Optional[str]
    firmware_filename: str
    uploaded_at: str
    
    class config:
        orm_mode = True


#response model for showing awailable firmwares:
class showFirmwares(BaseModel):
    firmware_name : str
    firmware_version : str
    firmware_filename : str
    firmware_target_devices : Optional[str]  
        
    class config:
        orm_mode = True
    