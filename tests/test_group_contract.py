import requests
from faker import Faker

from logger.logger import Logger
from services.university.helpers.group_helper import GroupHelper

faker = Faker()


class TestGroupContract:
    def test_create_group_anonym(self, university_api_utils_anonym):

        Logger.step("### Step 1. Create a group anonymously")
        group_helper = GroupHelper(api_utils=university_api_utils_anonym)
        response = group_helper.post_group({"name": faker.word()})

        Logger.step("### Step 2. Check that a group was not created")
        assert response.status_code == requests.status_codes.codes.unauthorized, (
            f"Wrong status code. Actual: '{response.status_code},"
            f" but expected: '{requests.status_codes.codes.unauthorized}'"
        )

    def test_get_group_admin(self, university_api_utils_admin):
        Logger.step("### Step 1. Get groups as an admin")
        group_helper = GroupHelper(api_utils=university_api_utils_admin)
        response = group_helper.get_groups()

        Logger.step("### Step 2. Check the response")
        assert response.status_code == requests.status_codes.codes.ok, (
            f"Wrong status code, Actual: '{response.status_code}',"
            f"but expect '{requests.status_codes.codes.ok}'"
        )

    def test_get_group_id_authorized(self, university_api_utils_admin):
        Logger.step("### Step 1. Get group by id as an authorized user")
        group_helper = GroupHelper(api_utils=university_api_utils_admin)
        response = group_helper.get_group(group_id=1)

        Logger.step("### Step 2. Check the response status code")
        assert response.status_code == requests.status_codes.codes.ok, (
            f"Wrong status code, Actual: '{response.status_code}',"
            f"but expect '{requests.status_codes.codes.ok}'"
        )
