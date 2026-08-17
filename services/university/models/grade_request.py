from pydantic import BaseModel

from services.university.models.base_grade import BaseGrade


class GradeRequest(BaseGrade):
    pass


class GradeQueryParams(BaseModel):
    student_id: int | None = None
    teacher_id: int | None = None
    group_id: int | None = None
