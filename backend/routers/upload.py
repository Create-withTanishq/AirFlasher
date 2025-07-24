from fastapi import APIRouter ,UploadFile ,File , Form
from typing import Annotated

router = APIRouter(
    prefix= "/upload",
    tags = ["Upload"]
)

@router.post("/")
async def get_firmware(
    firmware_file : Annotated[UploadFile, File()],
    firmware_name : Annotated[str, Form()],
    firmware_version : Annotated[str, Form()],
    firmware_description : Annotated[str, Form()],
    firmware_target_devices : Annotated[str, Form()],
):
    return {
        "firmware_name" : firmware_name,
        "firmware_version" : firmware_version,
        "firmware_description" : firmware_description,
        "firmware_target_devices" : firmware_target_devices,
        "firmware_filetype" : firmware_file.content_type
    }