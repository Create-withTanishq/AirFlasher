from fastapi import APIRouter ,UploadFile ,File , Form,Depends
from typing import Annotated
from sqlalchemy.orm import Session
from .. import schemas
import os
from datetime import datetime,timezone 
from ..utils import file_handler as fh
from .. database import get_db
from .. import models

router = APIRouter(
    prefix= "/upload",
    tags = ["Upload"]
)

UPLOAD_DIR = "static/firmware"

@router.post("/" , response_model= schemas.FirmwareUploadResponse)
async def get_firmware(
    firmware_file : Annotated[UploadFile, File()],
    firmware_name : Annotated[str, Form()],
    firmware_version : Annotated[str, Form()],
    firmware_description : Annotated[str, Form()],
    firmware_target_devices : Annotated[str, Form()],
    db : Session = Depends(get_db)
    ):
    
    firmware_filename,upload_time = await fh.save_firmware_file(firmware_file)
    new_firmware = models.firmwareInfo(
            firmware_name = firmware_name,
            firmware_version = firmware_version,
            firmware_description = firmware_description,
            firmware_target_devices = firmware_target_devices,
            firmware_filename = firmware_filename,
            upload_time  = upload_time
    )
    
    # adding new firmware to database
    db.add(new_firmware)
    
    # commiting the changes
    db.commit()
    
    #refreshing the database
    db.refresh(new_firmware)    
    
    return {
        "firmware_name" : firmware_name,
        "firmware_version" : firmware_version,
        "firmware_description" : firmware_description,
        "firmware_target_devices" : firmware_target_devices,
        "firmware_filename" : firmware_filename,
        "uploaded_at" : upload_time
    }