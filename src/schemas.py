from datetime import datetime, date
from typing import Optional

from pydantic import BaseModel, EmailStr, constr


class UserBaseSchema(BaseModel):
    name: str
    email: EmailStr
    photo: str

    class Config:
        orm_mode = True


class CreateUserSchema(UserBaseSchema):
    password: constr(min_length=8)
    passwordConfirm: str
    role: str = 'user'
    verified: bool = False


class UpdateUserSchema(BaseModel):
    name: str
    email: EmailStr
    photo: str

    class Config:
        orm_mode = True


class UpdateUserPasswordSchema(BaseModel):
    user_id: int
    password: constr(min_length=8)
    passwordConfirm: str


class LoginUserSchema(BaseModel):
    email: EmailStr
    password: constr(min_length=8)


class UserEmailSchema(BaseModel):
    email: EmailStr


class UserResponse(UserBaseSchema):
    id: int
    created_at: datetime
    updated_at: datetime


class PositionBaseSchema(BaseModel):
    title: str
    category: str
    company: str
    status: str
    created_by_id: int

    class Config:
        orm_mode = True


class PositionFullSchema(PositionBaseSchema):
    job_text: str
    salary: str


class PositionResponse(PositionFullSchema):
    created_at: datetime


class PositionShortVariantsSchema(BaseModel):
    title: str
    company: str

    class Config:
        orm_mode = True


class CandidateShortSchema(BaseModel):
    name: str
    date_applied: date
    career_site: str
    position_title: str
    status: str

    class Config:
        orm_mode = True


class CandidateTodaySchema(BaseModel):
    name: str
    position_title: str
    status: str

    class Config:
        orm_mode = True


class CandidateCreateSchema(BaseModel):
    name: str
    email: EmailStr
    phone_number: str
    created_by_id: int | None
    # Optional[constr(strip_whitespace=True,
    #                               regex=r"^(\+)[1-9][0-9\-\(\)\.]{9,15}$", )]
    github_link: str
    linkedin_link: str
    career_site: str
    date_applied: date
    status: str
    position_id: int

    class Config:
        orm_mode = True


class CandidateFullSchema(BaseModel):
    name: str
    email: EmailStr
    phone_number: str
    created_by_id: int | None
    # Optional[constr(strip_whitespace=True,
    #                               regex=r"^(\+)[1-9][0-9\-\(\)\.]{9,15}$", )]
    github_link: str
    linkedin_link: str
    career_site: str
    date_applied: date
    status: str
    position_title: str

    class Config:
        orm_mode = True


class CandidateUpdateSchema(BaseModel):
    name: str
    email: EmailStr
    phone_number: str
    # Optional[constr(strip_whitespace=True,
    #                               regex=r"^(\+)[1-9][0-9\-\(\)\.]{9,15}$", )]

    github_link: str
    linkedin_link: str
    status: str

    class Config:
        orm_mode = True


class CandidateUpdateStatusSchema(BaseModel):
    status: str

    class Config:
        orm_mode = True


class ScheduleBaseSchema(BaseModel):
    title: str
    text: str
    time_start: datetime
    time_end: datetime
    status: str
    created_by_id: int

    class Config:
        orm_mode = True


class ScheduleUpdateSchema(BaseModel):
    title: str
    text: str
    time_start: datetime
    time_end: datetime
    status: str

    class Config:
        orm_mode = True
