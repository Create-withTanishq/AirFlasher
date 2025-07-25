from sqlalchemy import Column , Integer , String , DateTime, Boolean
from datetime import datetime
from . database import Base

class firmwareInfo(Base):
    __tablename__ = "fimrware info"
    id = Column(Integer,primary_key= True , index= True)
    firmware_name = Column(String)
    firmware_filename = Column(String , unique= True , index= True)
    firmware_version = Column(String)
    firmware_description = Column(String)
    firmware_target_devices = Column(String)
    upload_time  = Column(String)
    update_mode = Column(Boolean , default= False)
    

