from services.university.models.base_grade import BaseGrade


class GradeRequest(BaseGrade):
    group_id: int
