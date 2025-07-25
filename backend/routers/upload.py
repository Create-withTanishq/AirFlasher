from fastapi import APIRouter ,UploadFile ,File , Form,Depends, HTTPException, status
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


@router.post("/" , response_model= schemas.FirmwareUploadResponse)
async def upload_firmware(
    firmware_file : Annotated[UploadFile, File()],
    firmware_name : Annotated[str, Form()],
    firmware_version : Annotated[str, Form()],
    firmware_description : Annotated[str, Form()],
    firmware_target_devices : Annotated[str, Form()],
    db : Session = Depends(get_db)
    ):
    # Check file extension
    if not firmware_file.filename.endswith(".bin"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only .bin firmware files are allowed!"
        )

    # checking file media type
    if firmware_file.content_type != "application/octet-stream":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid file type!"
        )
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