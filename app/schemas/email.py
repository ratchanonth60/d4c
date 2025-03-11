from typing import List, Optional

from pydantic import BaseModel, EmailStr


class EmailSchema(BaseModel):
    recipients: List[EmailStr]
    subject: str
    body: str
    cc: Optional[List[EmailStr]] = None
    bcc: Optional[List[EmailStr]] = None
    html_content: Optional[str] = None
