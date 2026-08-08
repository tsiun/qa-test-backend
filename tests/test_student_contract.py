import random

from faker import Faker
import requests

from services.university.helpers.student_helper import StudentHelper
from services.university.models.base_student import DegreeEnum
from services.university.models.student_request import StudentRequest
from services.university.models.student_response import StudentResponse

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

    def test_check_students_authorize(self, university_api_utils_admin):
        student_helper = StudentHelper(university_api_utils_admin)
        response = student_helper.get_students()

        assert response.status_code == requests.status_codes.codes.ok, (
            f"Wrong status code, Actual: '{response.status_code}',"
            f"but expect '{requests.status_codes.codes.ok}'"
        )

    def test_check_student_id_authorize(self, university_api_utils_admin):
        student_helper = StudentHelper(university_api_utils_admin)
        response = student_helper.get_student(student_id=1)

        assert response.status_code == requests.status_codes.codes.ok, (
            f"Wrong status code, Actual: '{response.status_code}',"
            f"but expect '{requests.status_codes.codes.ok}'"
        )
