import random

from faker import Faker

from logger.logger import Logger
from services.university.models.base_student import DegreeEnum
from services.university.models.group_request import GroupRequest
from services.university.models.student_request import StudentRequest
from services.university.university_service import UniversityService

faker = Faker()


class TestStudentCreate:
    def test_create_student_admin(self, university_api_utils_admin):
        Logger.step("### Step 1. Create group")
        university_service = UniversityService(api_utils=university_api_utils_admin)
        group = GroupRequest(name=faker.word())
        group_response = university_service.create_group(group_request=group)

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

        Logger.step("Check that the student is linked to the created group")

        assert student_response.group_id == group_response.id, (
            f"Wrong group id. Actual: '{student_response.group_id}',"
            f"but expected '{group_response.id}'"
        )

    def test_create_student_by_admin(self, student_data):
        Logger.step("Check that the student is created by admin")

        assert student_data.id is not None, (
            f"The student wasn't create, Actual: 'None', but expected: '{student_data.id}'"
        )

    def test_create_student_in_group(self, group_data, student_data):
        Logger.step("Check that the student is created in the group")

        assert student_data.group_id == group_data.id, (
            f"Wrong student id, Actual: '{student_data.group_id}', but expected: '{group_data.id}'"
        )
