import random

from faker import Faker
import requests

from logger.logger import Logger
from services.university import university_service
from services.university.helpers.teacher_helper import TeacherHelper
from services.university.models.base_teacher import SubjectEnum
from services.university.models.teacher_request import TeacherRequest

faker = Faker()


class TestTeacherContract:
    def test_create_teacher_anonym(self, university_api_utils_anonym):
        Logger.step("### Step 1. Create a teacher anonymously")
        teacher_helper = TeacherHelper(api_utils=university_api_utils_anonym)
        teacher = TeacherRequest(
            first_name=faker.first_name(),
            last_name=faker.last_name(),
            subject=random.choice(list(SubjectEnum)),
        )
        teacher_response = teacher_helper.post_teacher(json=teacher.model_dump())

        Logger.step("### Step 2. Check that a teacher was not created")

        assert (
            teacher_response.status_code == requests.status_codes.codes.unauthorized
        ), (
            f"Wrong status code. Actual: '{teacher_response.status_code}',"
            f"bud expected: '{requests.status_codes.codes.ok}'"
        )

    def test_create_teacher_admin(self, university_api_utils_admin):
        Logger.step("### Step 1. Create a teacher as an admin")
        teacher_helper = TeacherHelper(api_utils=university_api_utils_admin)
        teacher = TeacherRequest(
            first_name=faker.first_name(),
            last_name=faker.last_name(),
            subject=random.choice(list(SubjectEnum)),
        )
        teacher_response = teacher_helper.post_teacher(json=teacher.model_dump())

        Logger.step("### Step 2. Check the response status code")
        assert teacher_response.status_code == requests.status_codes.codes.created, (
            f"Wrong status code. Actual: '{teacher_response.status_code}',"
            f"bud expected: '{requests.status_codes.codes.ok}'"
        )
