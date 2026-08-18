import random
import time

import pytest
import requests

from services.auth.auth_service import AuthService
from services.auth.models.login_request import LoginRequest
from services.auth.models.register_request import RegisterRequest
from services.university.helpers.grade_helper import GradeHelper
from services.university.helpers.group_helper import GroupHelper
from services.university.helpers.student_helper import StudentHelper
from services.university.helpers.teacher_helper import TeacherHelper
from services.university.models.base_grade import MAX_GRADE, MIN_GRADE
from services.university.models.base_student import DegreeEnum
from services.university.models.base_teacher import SubjectEnum
from services.university.models.grade_request import GradeRequest
from services.university.models.group_request import GroupRequest
from services.university.models.student_request import StudentRequest
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


@pytest.fixture(scope="function", autouse=False)
def group_data(university_api_utils_admin):
    university_service = UniversityService(api_utils=university_api_utils_admin)
    group = GroupRequest(name=faker.word())
    group_data = university_service.create_group(group_request=group)
    yield group_data
    university_service.delete_group(group_id=group_data.id)


@pytest.fixture(scope="function", autouse=False)
def group_response(university_api_utils_admin):
    group_helper = GroupHelper(api_utils=university_api_utils_admin)
    group_response = group_helper.post_group({"name": faker.word()})
    yield group_response
    group_helper.delete_group(group_id=group_response.json()["id"])


@pytest.fixture(scope="function", autouse=False)
def student_data(university_api_utils_admin, group_data):
    university_service = UniversityService(api_utils=university_api_utils_admin)
    student = StudentRequest(
        first_name=faker.first_name(),
        last_name=faker.last_name(),
        email=faker.email(),
        degree=random.choice([option for option in DegreeEnum]),
        phone=faker.numerify("+7##########"),
        group_id=group_data.id,
    )
    student_data = university_service.create_student(student_request=student)
    yield student_data
    university_service.delete_student(student_id=student_data.id)


@pytest.fixture(scope="function", autouse=False)
def student_response(university_api_utils_admin, group_data):
    student_helper = StudentHelper(api_utils=university_api_utils_admin)
    student_response = student_helper.post_student(
        {
            "first_name": faker.first_name(),
            "last_name": faker.last_name(),
            "email": faker.email(),
            "degree": random.choice([option for option in DegreeEnum]),
            "phone": faker.numerify("+7##########"),
            "group_id": group_data.id,
        }
    )
    yield student_response
    student_helper.delete_student(student_id=student_response.json()["id"])


@pytest.fixture(scope="function", autouse=False)
def teacher_data(university_api_utils_admin):
    university_service = UniversityService(api_utils=university_api_utils_admin)
    teacher = TeacherRequest(
        first_name=faker.first_name(),
        last_name=faker.last_name(),
        subject=random.choice(list(SubjectEnum)),
    )
    teacher_data = university_service.create_teacher(teacher_request=teacher)
    yield teacher_data
    university_service.delete_teacher(teacher_id=teacher_data.id)


@pytest.fixture(scope="function", autouse=False)
def teacher_response(university_api_utils_admin):
    teacher_helper = TeacherHelper(api_utils=university_api_utils_admin)
    teacher_response = teacher_helper.post_teacher(
        {
            "first_name": faker.first_name(),
            "last_name": faker.last_name(),
            "subject": random.choice(list(SubjectEnum)),
        }
    )
    yield teacher_response
    teacher_helper.delete_teacher(teacher_id=teacher_response.json()["id"])


@pytest.fixture(scope="function", autouse=False)
def grade_data(university_api_utils_admin, teacher_data, student_data):
    university_service = UniversityService(api_utils=university_api_utils_admin)
    grade = GradeRequest(
        teacher_id=teacher_data.id,
        student_id=student_data.id,
        grade=random.randint(a=MIN_GRADE, b=MAX_GRADE),
    )
    grade_data = university_service.create_grade(grade_request=grade)
    yield grade_data
    university_service.delete_grade(grade_id=grade_data.id)


@pytest.fixture(scope="function", autouse=False)
def grade_response(university_api_utils_admin, teacher_data, student_data):
    grade_helper = GradeHelper(api_utils=university_api_utils_admin)
    grade_response = grade_helper.post_grade(
        {
            "teacher_id": teacher_data.id,
            "student_id": student_data.id,
            "grade": random.randint(a=MIN_GRADE, b=MAX_GRADE),
        }
    )
    yield grade_response
    grade_helper.delete_grade(grade_id=grade_response.json()["id"])
