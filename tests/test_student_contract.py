import random

from faker import Faker
import requests

from logger.logger import Logger
from services.university.helpers.student_helper import StudentHelper
from services.university.models.base_student import DegreeEnum
from services.university.models.group_request import GroupRequest
from services.university.models.student_request import StudentRequest
from services.university.models.student_response import StudentResponse
from services.university.university_service import UniversityService

faker = Faker()


class TestStudentContract:
    def test_create_student_anonym(self, university_api_utils_anonym):
        student_helper = StudentHelper(api_utils=university_api_utils_anonym)
        student = StudentRequest(
            first_name=faker.first_name(),
            last_name=faker.last_name(),
            email=faker.email(),
            degree=random.choice(list(DegreeEnum)),
            phone=faker.numerify("+7##########"),
            group_id=1,
        )
        response = student_helper.post_student(json=student.model_dump())

        assert response.status_code == requests.status_codes.codes.unauthorized, (
            f"Wrong status code, Actual: '{response.status_code}',"
            f"but expect '{requests.status_codes.codes.unauthorized}'"
        )

    def test_check_students_admin(self, university_api_utils_admin):
        student_helper = StudentHelper(university_api_utils_admin)
        response = student_helper.get_students()

        assert response.status_code == requests.status_codes.codes.ok, (
            f"Wrong status code, Actual: '{response.status_code}',"
            f"but expect '{requests.status_codes.codes.ok}'"
        )

    def test_check_student_id_admin(self, university_api_utils_admin):
        Logger.info("### Step 1. Create group")
        university_service = UniversityService(api_utils=university_api_utils_admin)
        group = GroupRequest(name=faker.word())
        group_response = university_service.create_group(group_request=group)
        group_id = group_response.id

        Logger.info("### Step 2. Create student")
        student = StudentRequest(
            first_name=faker.first_name(),
            last_name=faker.last_name(),
            email=faker.email(),
            degree=random.choice([option for option in DegreeEnum]),
            phone=faker.numerify("+7##########"),
            group_id=group_id,
        )
        student_response = university_service.create_student(student_request=student)
        student_id = student_response.id

        Logger.info("### Step 3. Compare the actual student id with expected")
        actual_student = university_service.get_student(student_id=student_id)

        assert actual_student.id == student_id, (
            f"Invalid student ID generated, Actual: '{actual_student.id}',"
            f"but expect '{student_id}'"
        )

        assert actual_student.group_id == group_id, (
            f"Invalid group ID generated, Actual: '{actual_student.group_id}',"
            f"but expect '{group_id}'"
        )
