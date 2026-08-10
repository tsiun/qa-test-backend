from faker import Faker
import requests

from services.university.helpers.grade_helper import GradeHelper
from services.university.models.grade_request import GradeRequest


faker = Faker()


class TestGradeContract:
    def test_create_grade_authorized(self, university_api_utils_admin):
        grade_helper = GradeHelper(api_utils=university_api_utils_admin)
        grade = GradeRequest(
            teacher_id=faker.random_int(),
            student_id=faker.random_int(),
            grade=faker.random_int(min=1, max=5),
        )

        response = grade_helper.post_grade(json=grade.model_dump())

        assert response.status_code == requests.status_codes.codes.created, (
            f"Wrong status code, Actual: '{requests.status_codes.codes.created}',"
            f"but got '{response.status_code}'"
        )
