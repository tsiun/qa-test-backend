import random

from faker import Faker

from logger.logger import Logger
from services.university.models.base_student import DegreeEnum
from services.university.models.base_teacher import SubjectEnum
from services.university.models.grade_request import GradeRequest
from services.university.models.group_request import GroupRequest
from services.university.models.student_request import StudentRequest
from services.university.models.teacher_request import TeacherRequest
from services.university.university_service import UniversityService
from services.university.models.base_grade import MIN_GRADE, MAX_GRADE

faker = Faker()


class TestTeacher:
    def test_teacher_gives_a_grade_admin(self, university_api_utils_admin):
        Logger.info("### Step 1. Create group")
        university_service = UniversityService(api_utils=university_api_utils_admin)
        group = GroupRequest(name=faker.word())
        group_response = university_service.create_group(group_request=group)

        Logger.info("### Step 2. Create teacher")
        university_service = UniversityService(api_utils=university_api_utils_admin)
        teacher = TeacherRequest(
            first_name=faker.first_name(),
            last_name=faker.last_name(),
            subject=random.choice(list(SubjectEnum)),
        )
        teacher_response = university_service.create_teacher(teacher_request=teacher)

        Logger.info("### Step 3. Create student")
        student = StudentRequest(
            first_name=faker.first_name(),
            last_name=faker.last_name(),
            email=faker.email(),
            degree=random.choice([option for option in DegreeEnum]),
            phone=faker.numerify("+7##########"),
            group_id=group_response.id,
        )
        student_response = university_service.create_student(student_request=student)

        Logger.info("### Step 4. The teacher gives a grade")
        grade = GradeRequest(
            teacher_id=teacher_response.id,
            student_id=student_response.id,
            grade=random.randint(MIN_GRADE, MAX_GRADE),
            group_id=group_response.id,
        )
        grade_response = university_service.create_grade(grade_request=grade)

        assert grade_response.teacher_id == teacher_response.id, (
            f"Wrong teacher id. Actual: '{grade_response.teacher_id}',"
            f"bud expected: '{teacher_response.id}'"
        )

    def test_get_list_of_teachers(self, university_api_utils_admin):
        Logger.info("### Step 1. Create a teacher")
        university_service = UniversityService(api_utils=university_api_utils_admin)
        teacher = TeacherRequest(
            first_name=faker.first_name(),
            last_name=faker.last_name(),
            subject=random.choice(list(SubjectEnum)),
        )
        teacher_response = university_service.create_teacher(teacher_request=teacher)
        teacher_id = teacher_response.id

        Logger.info("### Step 2. Get list of teachers ")
        university_service = UniversityService(api_utils=university_api_utils_admin)
        teachers = university_service.get_teachers()
        teacher_ids = [teacher.id for teacher in teachers]

        assert teacher_id in teacher_ids
