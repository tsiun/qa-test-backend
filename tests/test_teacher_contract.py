import random

from faker import Faker

from services.university.helpers.teacher_helper import TeacherHelper
from services.university.models.base_teacher import SubjectEnum
from services.university.models.teacher_request import TeacherRequest

faker = Faker()


class TestTeacherContract:
    def test_create_teacher_authorized(self, university_api_utils_admin):
        teacher_helper = TeacherHelper(api_utils=university_api_utils_admin)
        teacher = TeacherRequest(
            first_name=faker.first_name(),
            last_name=faker.last_name(),
            subject=random.choice(list(SubjectEnum)),
        )
