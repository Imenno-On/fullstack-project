from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field, HttpUrl, conint, model_validator


class TestStatus(str, Enum):
    ACTIVE = "active"
    COMPLETED = "completed"


class TestBase(BaseModel):
    title: str = Field(..., min_length=3, max_length=100)
    date: str = Field(..., min_length=3, max_length=50, description="Дата отображения на фронте")
    link: HttpUrl = Field(..., description="Яндекс.Форма или иной URL теста")
    students: conint(ge=0, le=5000) = Field(..., description="Количество учеников, приглашённых к тесту")
    completed: conint(ge=0, le=5000) = Field(..., description="Количество учеников, завершивших тест")
    status: TestStatus = Field(..., description="active или completed")
    description: Optional[str] = Field(None, max_length=500)

    @model_validator(mode="after")
    def ensure_completed_not_exceed_total(self):
        if self.completed > self.students:
            raise ValueError("completed must be less than or equal to students")
        return self


class TestCreate(TestBase):
    pass


class TestUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=3, max_length=100)
    date: Optional[str] = Field(None, min_length=3, max_length=50)
    link: Optional[HttpUrl] = None
    students: Optional[conint(ge=0, le=5000)] = None
    completed: Optional[conint(ge=0, le=5000)] = None
    status: Optional[TestStatus] = None
    description: Optional[str] = Field(None, max_length=500)

    @model_validator(mode="after")
    def ensure_completed_not_exceed_total(self):
        if self.completed is not None and self.students is not None:
            if self.completed > self.students:
                raise ValueError("completed must be less than or equal to students")
        return self


class Test(TestBase):
    id: int

