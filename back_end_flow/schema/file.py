from pydantic import BaseModel
from datetime import datetime

class FileNameInput(BaseModel):
    file_name: str

class FileResponse(BaseModel):
    file_name: str
    timestamp: datetime
   
