from pydantic import TypeAdapter

from services.general.base_service import BaseService
from services.university.helpers.grade_helper import GradeHelper
from services.university.helpers.group_helper import GroupHelper
from services.university.helpers.student_helper import StudentHelper
from services.university.helpers.teacher_helper import TeacherHelper
from services.university.models.grade_request import GradeRequest, GradeQueryParams
from services.university.models.grade_response import GradeResponse
from services.university.models.grade_stats_response import GradeStatsResponse
from services.university.models.group_request import GroupRequest
from services.university.models.group_response import GroupResponse
from services.university.models.student_request import StudentRequest
from services.university.models.student_response import StudentResponse
from services.university.models.teacher_request import TeacherRequest
from services.university.models.teacher_response import TeacherResponse
from utils.api_utils import ApiUtils


class UniversityService(BaseService):
    SERVICE_URL = "http://127.0.0.1:8001"

    def __init__(self, api_utils: ApiUtils) -> None:
        super().__init__(api_utils)

        self.group_helper = GroupHelper(self.api_utils)
        self.student_helper = StudentHelper(self.api_utils)
        self.teacher_helper = TeacherHelper(self.api_utils)
        self.grade_helper = GradeHelper(self.api_utils)

    def create_group(self, group_request: GroupRequest) -> GroupResponse:
        response = self.group_helper.post_group(json=group_request.model_dump())
        return GroupResponse(**response.json())

    def get_groups(self) -> list[GroupResponse]:
        response = self.group_helper.get_groups()
        groups_adapter = TypeAdapter(list[GroupResponse])
        return groups_adapter.validate_python(response.json())

    def get_group(self, group_id: int) -> GroupResponse:
        response = self.group_helper.get_group(group_id=group_id)
        return GroupResponse(**response.json())

    def delete_group(self, group_id: int) -> GroupResponse:
        response = self.group_helper.delete_group(group_id=group_id)
        return GroupResponse(**response.json())

    def update_group(self, group_request: GroupRequest, group_id: int) -> GroupResponse:
        response = self.group_helper.put_group(
            json=group_request.model_dump(), group_id=group_id
        )
        return GroupResponse(**response.json())

    def create_student(self, student_request: StudentRequest) -> StudentResponse:
        response = self.student_helper.post_student(json=student_request.model_dump())
        return StudentResponse(**response.json())

    def get_students(self) -> list[StudentResponse]:
        response = self.student_helper.get_students()
        students_adapter = TypeAdapter(list[StudentResponse])
        return students_adapter.validate_python(response.json())

    def get_student(self, student_id: int) -> StudentResponse:
        response = self.student_helper.get_student(student_id=student_id)
        return StudentResponse(**response.json())

    def delete_student(self, student_id: int) -> StudentResponse:
        response = self.student_helper.delete_student(student_id=student_id)
        return StudentResponse(**response.json())

    def update_student(
            self, student_request: StudentRequest, student_id: int
    ) -> StudentResponse:
        response = self.student_helper.put_student(
            student_id=student_id, json=student_request.model_dump()
        )
        return StudentResponse(**response.json())

    def create_teacher(self, teacher_request: TeacherRequest) -> TeacherResponse:
        response = self.teacher_helper.post_teacher(json=teacher_request.model_dump())
        return TeacherResponse(**response.json())

    def get_teachers(self) -> list[TeacherResponse]:
        response = self.teacher_helper.get_teachers()
        teachers_adapter = TypeAdapter(list[TeacherResponse])
        return teachers_adapter.validate_python(response.json())

    def get_teacher(self, teacher_id: int) -> TeacherResponse:
        response = self.teacher_helper.get_teacher(teacher_id=teacher_id)
        return TeacherResponse(**response.json())

    def delete_teachers(self, teacher_id: int) -> TeacherResponse:
        response = self.teacher_helper.delete_teacher(teacher_id=teacher_id)
        return TeacherResponse(**response.json())

    def update_teacher(
            self, teacher_request: TeacherRequest, teacher_id: int
    ) -> TeacherResponse:
        response = self.teacher_helper.put_teacher(
            teacher_id=teacher_id, json=teacher_request.model_dump()
        )
        return TeacherResponse(**response.json())

    def create_grade(self, grade_request: GradeRequest) -> GradeResponse:
        response = self.grade_helper.post_grade(data=grade_request.model_dump())
        return GradeResponse(**response.json())

    def get_grades(self, grade_params: GradeQueryParams) -> list[GradeResponse]:
        params = {k: v for k, v in grade_params.model_dump().items() if v is not None}
        response = self.grade_helper.get_grades(params=params)
        grades_adapter = TypeAdapter(list[GradeResponse])
        return grades_adapter.validate_python(response.json())

    def get_grade_stats(self, grade_params: GradeQueryParams) -> GradeStatsResponse:
        params = {k: v for k, v in grade_params.model_dump().items() if v is not None}
        response = self.grade_helper.get_grades_stats(params=params)
        return GradeStatsResponse(**response.json())

    def delete_grade(self, grade_id: int) -> GradeResponse:
        response = self.grade_helper.delete_grade(grade_id=grade_id)
        return GradeResponse(**response.json())

    def update_grade(self, grade_request: GradeRequest, grade_id: int) -> GradeResponse:
        response = self.grade_helper.put_grade(
            grade_id=grade_id, data=grade_request.model_dump()
        )
        return GradeResponse(**response.json())
