from fastapi import APIRouter,Depends,HTTPException, status
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from .. database import get_db
from .. import models, schemas
from typing import List
import os

router = APIRouter(
    prefix = "/firmware",
    tags = ["firmware"]
)

@router.get("/" , response_model= List[schemas.showFirmwares])
async def get_all_firmwares(db: Session = Depends(get_db)):
    firmwares = db.query(models.firmwareInfo).all()
    return firmwares
    
    
@router.get("/latest" , response_model= schemas.showFirmwares)
async def get_latest_firmware( db : Session = Depends(get_db)):
    firmware = db.query(models.firmwareInfo).order_by(models.firmwareInfo.id.desc()).first()
    return firmware


@router.put("/activate/{firmware_id}")
async def activateFirmware(firmware_id : int , db : Session = Depends(get_db)):
    firmware = db.query(models.firmwareInfo).filter(models.firmwareInfo.id == firmware_id).first()
    if not firmware:
        raise HTTPException(
            status_code= status.HTTP_404_NOT_FOUND,
            detail = f"Firmware with {firmware_id} not found !!"
        )
    firmware.update_mode = True
    #saving changes
    db.commit()
    db.refresh(firmware)
    
    return {
        "message" : f"Firmware with ID:{firmware_id} is now set for OTA update."
    }


@router.get("/download")
async def download_firmware(db : Session = Depends(get_db)):
    dwn_firmware = db.query(models.firmwareInfo).filter(models.firmwareInfo.update_mode == True).first()
    if not dwn_firmware :
        raise HTTPException(
            status_code= status.HTTP_204_NO_CONTENT,
            detail = "No Firmware found that is ready to be Upoaded !" 
        )
    
    file_path = f"backend/static/firmware/{dwn_firmware.firmware_filename}"
    if not os.path.exists(file_path):
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "Firmware File not found !"
        )
        
        
    # making the firmware back to not active
    dwn_firmware.update_mode =False
    db.commit()
    db.refresh(dwn_firmware)
    
    return FileResponse(
        path = file_path,
        status_code= status.HTTP_202_ACCEPTED,
        filename = dwn_firmware.firmware_filename,
        media_type = "application/octet-stream"
        )
    
    
    

