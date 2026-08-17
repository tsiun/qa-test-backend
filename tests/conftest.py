import random
import time

import pytest
import requests

from services.auth.auth_service import AuthService
from services.auth.models.login_request import LoginRequest
from services.auth.models.register_request import RegisterRequest
from services.university.helpers.group_helper import GroupHelper
from services.university.helpers.teacher_helper import TeacherHelper
from services.university.models.base_teacher import SubjectEnum
from services.university.models.group_request import GroupRequest
from services.university.models.teacher_request import TeacherRequest
from services.university.university_service import UniversityService
from utils.api_utils import ApiUtils
from faker import Faker

faker = Faker()


@pytest.fixture(scope="function", autouse=True)
def auth_service_readiness():
    timeout = 180
    start_time = time.time()
    while time.time() < start_time + timeout:
        try:
            response = requests.get(AuthService.SERVICE_URL + "/docs")
            response.raise_for_status()
        except:
            time.sleep(1)
        else:
            break
    else:
        raise RuntimeError(f"Auth service wasn't started during {timeout} seconds")


@pytest.fixture(scope="function", autouse=False)
def auth_api_utils_anonym():
    api_utils = ApiUtils(url=AuthService.SERVICE_URL)
    return api_utils


@pytest.fixture(scope="function", autouse=False)
def university_api_utils_anonym():
    api_utils = ApiUtils(url=UniversityService.SERVICE_URL)
    return api_utils


@pytest.fixture(scope="function", autouse=False)
def access_token(auth_api_utils_anonym):
    auth_service = AuthService(auth_api_utils_anonym)
    username = faker.user_name()
    password = faker.password(
        length=30, special_chars=True, digits=True, upper_case=True, lower_case=True
    )
    auth_service.register_user(
        register_request=RegisterRequest(
            username=username,
            password=password,
            password_repeat=password,
            email=faker.email(),
        )
    )
    login_response = auth_service.login_user(
        login_request=LoginRequest(username=username, password=password)
    )
    return login_response.access_token


@pytest.fixture(scope="function", autouse=False)
def auth_api_utils_admin(access_token):
    api_utils = ApiUtils(
        url=AuthService.SERVICE_URL, headers={"Authorization": f"Bearer {access_token}"}
    )
    return api_utils


@pytest.fixture(scope="function", autouse=False)
def university_api_utils_admin(access_token):
    api_utils = ApiUtils(
        url=UniversityService.SERVICE_URL,
        headers={"Authorization": f"Bearer {access_token}"},
    )
    return api_utils


@pytest.fixture(scope="session", autouse=False)
def group_data(university_api_utils_admin):
    university_service = UniversityService(api_utils=university_api_utils_admin)
    group = GroupRequest(name=faker.word())
    group_data = university_service.create_group(group_request=group)
    return group_data


@pytest.fixture(scope="session", autouse=False)
def group_response(university_api_utils_admin):
    group_helper = GroupHelper(api_utils=university_api_utils_admin)
    group_response = group_helper.post_group({"name": faker.word()})
    return group_response


@pytest.fixture(scope="session", autouse=False)
def teacher_data(university_api_utils_admin):
    university_service = UniversityService(api_utils=university_api_utils_admin)
    teacher = TeacherRequest(
        first_name=faker.first_name(),
        last_name=faker.last_name(),
        subject=random.choice(list(SubjectEnum)),
    )
    teacher_data = university_service.create_teacher(teacher_request=teacher)
    return teacher_data


@pytest.fixture(scope="session", autouse=False)
def teacher_response(university_api_utils_admin):
    teacher_helper = TeacherHelper(api_utils=university_api_utils_admin)
    teacher_response = teacher_helper.post_teacher(
        {
            "first_name": faker.first_name(),
            "last_name": faker.last_name(),
            "subject": random.choice(list(SubjectEnum)),
        }
    )
    return teacher_response
