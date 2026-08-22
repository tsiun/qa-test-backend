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
    def test_get_stat_for_group(self, university_api_utils_admin, soft_assert):
        Logger.step("### Step 1. Create two groups")
        university_service = UniversityService(api_utils=university_api_utils_admin)

        group_1 = university_service.create_group(
            group_request=GroupRequest(name=faker.name())
        )
        group_2 = university_service.create_group(
            group_request=GroupRequest(name=faker.name())
        )

        Logger.step("### Step 2. Create two teachers")

        teacher_1 = university_service.create_teacher(
            teacher_request=TeacherRequest(
                first_name=faker.first_name(),
                last_name=faker.last_name(),
                subject=random.choice(list(SubjectEnum)),
            )
        )
        teacher_2 = university_service.create_teacher(
            teacher_request=TeacherRequest(
                first_name=faker.first_name(),
                last_name=faker.last_name(),
                subject=random.choice(list(SubjectEnum)),
            )
        )

        Logger.step("### Step 3. Create three students in two groups")

        student_1 = university_service.create_student(
            student_request=StudentRequest(
                first_name=faker.first_name(),
                last_name=faker.last_name(),
                email=faker.email(),
                degree=random.choice(list(DegreeEnum)),
                phone=faker.numerify("+7##########"),
                group_id=group_1.id,
            )
        )
        student_2 = university_service.create_student(
            student_request=StudentRequest(
                first_name=faker.first_name(),
                last_name=faker.last_name(),
                email=faker.email(),
                degree=random.choice(list(DegreeEnum)),
                phone=faker.numerify("+7##########"),
                group_id=group_1.id,
            )
        )
        student_3 = university_service.create_student(
            student_request=StudentRequest(
                first_name=faker.first_name(),
                last_name=faker.last_name(),
                email=faker.email(),
                degree=random.choice(list(DegreeEnum)),
                phone=faker.numerify("+7##########"),
                group_id=group_2.id,
            )
        )

        Logger.step("### Step 4. Create a grades for the student by teachers")
        grade_1 = university_service.create_grade(
            grade_request=GradeRequest(
                teacher_id=teacher_1.id,
                student_id=student_1.id,
                grade=random.randint(a=MIN_GRADE, b=MAX_GRADE),
            )
        )
        grade_2 = university_service.create_grade(
            grade_request=GradeRequest(
                teacher_id=teacher_2.id,
                student_id=student_1.id,
                grade=random.randint(a=MIN_GRADE, b=MAX_GRADE),
            )
        )
        grade_3 = university_service.create_grade(
            grade_request=GradeRequest(
                teacher_id=teacher_2.id,
                student_id=student_2.id,
                grade=random.randint(a=MIN_GRADE, b=MAX_GRADE),
            )
        )
        Logger.step("### Step 5. Count an expected average")
        expected_avg = (grade_1.grade + grade_2.grade) / 2

        Logger.step("### Step 6. Get statistics for group_1")
        stats_group_1 = university_service.get_grades_stats(group_id=group_1.id)

        soft_assert.check(
            stats_group_1.avg == expected_avg,
            (
                f"Wrong an average grade, Actual: '{stats_group_1.avg}', but expected '{expected_avg}'"
            ),
        )

        soft_assert.check(
            stats_group_1.count == 2,
            (
                f"Wrong the total count of grades in group_1, Actual: '{stats_group_1.count}', bud expected '{2}'"
            ),
        )

        Logger.step("### Step 7. Get statustics for group_2 (empty)")
        stats_group_2 = university_service.get_grades_stats(group_id=group_2.id)

        soft_assert.check(
            stats_group_2.count == 0,
            (
                f"Wrong the total coun of grades in group_2, Actual: '{stats_group_2.count}', but expected: '{0}'"
            ),
        )
