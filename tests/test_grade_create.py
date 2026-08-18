from faker import Faker
import random
import requests

from logger.logger import Logger
from services.university.helpers.grade_helper import GradeHelper
from services.university.models.base_grade import MIN_GRADE, MAX_GRADE
from services.university.models.base_student import DegreeEnum
from services.university.models.base_teacher import SubjectEnum
from services.university.models.grade_request import GradeRequest
from services.university.models.group_request import GroupRequest
from services.university.models.student_request import StudentRequest
from services.university.models.teacher_request import TeacherRequest
from services.university.university_service import UniversityService

faker = Faker()


class TestGradeCreate:
    def test_create_grade_admin(self, grade_data):
        assert grade_data.id is not None, (
            f"The grade wasn't given, Actual: 'None', but expected: '{grade_data.id}' "
        )

    def test_create_grade_by_teacher(self, grade_data, teacher_data):
        assert grade_data.teacher_id == teacher_data.id, (
            f"Wrong teacher id, Actual: '{grade_data.teacher_id}', but expected: '{teacher_data.id}'"
        )

    def test_create_grade_to_student(self, grade_data, student_data):
        assert grade_data.student_id == student_data.id, (
            f"Wrong student id, Actual: '{grade_data.student_id}', but expected: '{student_data.id}'"
        )
