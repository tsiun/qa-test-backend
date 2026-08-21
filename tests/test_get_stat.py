import random

from faker import Faker

from logger.logger import Logger
from services.university.models.base_grade import MAX_GRADE, MIN_GRADE
from services.university.models.base_student import DegreeEnum
from services.university.models.base_teacher import SubjectEnum
from services.university.models.grade_request import GradeRequest
from services.university.models.group_request import GroupRequest
from services.university.models.student_request import StudentRequest
from services.university.models.teacher_request import TeacherRequest
from services.university.university_service import UniversityService

faker = Faker()


class TestGetStat:
    def test_get_stat_for_group(self, university_api_utils_admin):
        Logger.step("### Step 1. Create two groups")
        university_service = UniversityService(api_utils=university_api_utils_admin)
        group_one = GroupRequest(name=faker.name())
        group_1 = university_service.create_group(group_request=group_one)
        group_2 = university_service.create_group(group_request=group)

        Logger.step("### Step 2. Create two teachers")
        university_service = UniversityService(api_utils=university_api_utils_admin)
        teacher = TeacherRequest(
            first_name=faker.first_name(),
            last_name=faker.last_name(),
            subject=random.choice(list(SubjectEnum)),
        )
        teacher_1 = university_service.create_teacher(teacher_request=teacher)
        teacher_2 = university_service.create_teacher(teacher_request=teacher)

        Logger.step("### Step 3. Create three students")
        student_one = StudentRequest(
            first_name=faker.first_name(),
            last_name=faker.last_name(),
            email=faker.email(),
            degree=random.choice([option for option in DegreeEnum]),
            phone=faker.numerify("+7##########"),
            group_id=group_1.id,
        )
        student_1 = university_service.create_student(student_request=student_one)
        student_2 = university_service.create_student(student_request=student)
        student_3 = university_service.create_student(student_request=student)

        Logger.step(
            "### Step 4. Prepare a grade request for: student_1 from group_1 gave grades from teacher_1 and teacher_2"
        )
        university_service = UniversityService(api_utils=university_api_utils_admin)
        grade_one = GradeRequest(
            teacher_id=teacher_1.id,
            student_id=student_1.id,
            grade=random.randint(a=MIN_GRADE, b=MAX_GRADE),
        )
        grade_two = GradeRequest(
            teacher_id=teacher_2.id,
            student_id=student_1.id,
            grade=random.randint(a=MIN_GRADE, b=MAX_GRADE),
        )

        Logger.step("### Step 5. Create a grade for the student by the teacher")
        grade_1 = university_service.create_grade(grade_request=grade_one)
