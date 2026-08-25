import random

from faker import Faker


from logger.logger import Logger
from services.university.models.base_grade import MAX_GRADE, MIN_GRADE
from services.university.models.base_student import DegreeEnum
from services.university.models.base_teacher import SubjectEnum
from services.university.models.grade_request import GradeRequest
from services.university.models.student_request import StudentRequest
from services.university.models.teacher_request import TeacherRequest
from services.university.university_service import UniversityService

faker = Faker()


class TestGradeCreate:
    def test_create_grade_admin(
        self, university_api_utils_admin, teacher_data, student_data
    ):
        Logger.step("### Step 1. Prepare data for a grade by admin")
        university_service = UniversityService(api_utils=university_api_utils_admin)
        grade = GradeRequest(
            teacher_id=teacher_data.id,
            student_id=student_data.id,
            grade=random.randint(a=MIN_GRADE, b=MAX_GRADE),
        )
        grade_data = university_service.create_grade(grade_request=grade)

        Logger.step("### Step 2. Check that the grade is created by admin")

        assert grade_data.id is not None, (
            f"The grade wasn't given, Actual: 'None', but expected: '{grade_data.id}' "
        )

    def test_create_grade_by_teacher(self, university_api_utils_admin, student_data):
        Logger.step("### Step 1. Prepare data for create teacher")

        university_service = UniversityService(api_utils=university_api_utils_admin)
        teacher = TeacherRequest(
            first_name=faker.first_name(),
            last_name=faker.last_name(),
            subject=random.choice(list(SubjectEnum)),
        )
        teacher_data = university_service.create_teacher(teacher_request=teacher)

        Logger.step("### Step 2. Prepare data for a grade by teacher")
        university_service = UniversityService(api_utils=university_api_utils_admin)
        grade = GradeRequest(
            teacher_id=teacher_data.id,
            student_id=student_data.id,
            grade=random.randint(a=MIN_GRADE, b=MAX_GRADE),
        )
        grade_data = university_service.create_grade(grade_request=grade)

        Logger.step("### Step 3. Check that the grade is given by teacher")
        assert grade_data.teacher_id == teacher_data.id, (
            f"Wrong teacher id, Actual: '{grade_data.teacher_id}', but expected: '{teacher_data.id}'"
        )

    def test_create_grade_to_student(
        self, university_api_utils_admin, teacher_data, student_data, group_data
    ):
        Logger.step("### Step 1. Prepare data for a grade to student")

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

        Logger.step("### Step 2. Prepare data for a grade for student")

        university_service = UniversityService(api_utils=university_api_utils_admin)
        grade = GradeRequest(
            teacher_id=teacher_data.id,
            student_id=student_data.id,
            grade=random.randint(a=MIN_GRADE, b=MAX_GRADE),
        )
        grade_data = university_service.create_grade(grade_request=grade)

        assert grade_data.student_id == student_data.id, (
            f"Wrong student id, Actual: '{grade_data.student_id}', but expected: '{student_data.id}'"
        )

    def test_create_grade_with_wrong_data(self, university_api_utils_admin):
        Logger.step("### Step 1. Prepare data for a grade with wrong data")

        university_service = UniversityService(api_utils=university_api_utils_admin)
        grade = GradeRequest(
            teacher_id=faker.randint(min=100, max=150),
            student_id=faker.randint(min=100, max=150),
            grade=random.randint(a=MIN_GRADE, b=MAX_GRADE),
        )
        grade_data = university_service.create_grade(grade_request=grade)

        assert grade_data == 404, (
            f"The grade was given with wrong data, Actual: '{grade_data}', but expected: '404'"
        )
