from faker import Faker

from logger.logger import Logger
from services.university.models.group_request import GroupRequest
from services.university.university_service import UniversityService

faker = Faker()


class TestGroupCreate:
    def test_create_group_by_admin(self, university_api_utils_admin):
        Logger.step("### Step 1. Create a group")
        university_service = UniversityService(api_utils=university_api_utils_admin)

        group = GroupRequest(name=faker.word())
        group_response = university_service.create_group(group_request=group)

        Logger.step("### Step 2. Check that a group was created")

        assert group_response.id is not None, (
            f"The group wasn't create, Actual: 'None', but expected: '{group_response.id}'"
        )

        Logger.step("### Step 3. Delete created group")
        university_service.delete_group(group_id=group_response.id)
