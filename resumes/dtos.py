from typing import Optional

from pydantic import BaseModel

from resumes.models import Resume


class ResumeDto(BaseModel):
    class Config:
        orm_mode = True
        model = Resume

    status: Optional[str]
    grade: Optional[str]
    specialty: Optional[str]
    salary: Optional[int]
    education: Optional[str]
    experience: Optional[str]
    portfolio: Optional[str]
    title: Optional[str]
    phone: Optional[str]
    email: Optional[str]
