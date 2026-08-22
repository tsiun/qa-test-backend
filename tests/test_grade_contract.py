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


class TestGradeContract:
    def test_create_grade_admin(self, university_api_utils_admin):
        Logger.step("### Step 1. Create group")
        university_service = UniversityService(api_utils=university_api_utils_admin)
        group = GroupRequest(name=faker.word())
        group_response = university_service.create_group(group_request=group)
        group_id = group_response.id

        Logger.step("### Step 2. Create student")
        student = StudentRequest(
            first_name=faker.first_name(),
            last_name=faker.last_name(),
            email=faker.email(),
            degree=random.choice([option for option in DegreeEnum]),
            phone=faker.numerify("+7##########"),
            group_id=group_response.id,
        )
        student_response = university_service.create_student(student_request=student)
        student_id = student_response.id

        Logger.step("### Step 3. Create a teacher")
        university_service = UniversityService(api_utils=university_api_utils_admin)
        teacher = TeacherRequest(
            first_name=faker.first_name(),
            last_name=faker.last_name(),
            subject=random.choice(list(SubjectEnum)),
        )
        teacher_response = university_service.create_teacher(teacher_request=teacher)
        teacher_id = teacher_response.id

        Logger.step("### Step 4. Create a grade")
        grade_helper = GradeHelper(api_utils=university_api_utils_admin)
        grade = GradeRequest(
            teacher_id=teacher_id,
            student_id=student_id,
            grade=random.randint(a=MIN_GRADE, b=MAX_GRADE),
            # group_id=group_id,
        )

        response = grade_helper.post_grade(data=grade.model_dump())

        assert response.status_code == requests.status_codes.codes.created, (
            f"Wrong status code, Actual: '{requests.status_codes.codes.created}',"
            f"but got '{response.status_code}'"
        )
