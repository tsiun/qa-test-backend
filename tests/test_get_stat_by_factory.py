from logger.logger import Logger
from services.university.university_service import UniversityService


class TestGetStatBusinessLogic:
    def test_average_calculation(
        self,
        university_api_utils_admin,
        teacher_factory,
        student_factory,
        group_factory,
        grade_factory,
    ):
        Logger.step("### Step 1. Prepare a group, teacher, and student")
        university_service = UniversityService(api_utils=university_api_utils_admin)
        group = group_factory()
        teacher = teacher_factory()
        student = student_factory(group_id=group.id)

        Logger.step("### Step 2. Give exact grades for check the calculation")
        grade_1 = grade_factory(teacher_id=teacher.id, student_id=student.id, grade=3)
        grade_2 = grade_factory(teacher_id=teacher.id, student_id=student.id, grade=4)
        grade_3 = grade_factory(teacher_id=teacher.id, student_id=student.id, grade=5)

        Logger.step("### Step 3. Calculate an expected result")
        expected_avg = (grade_1.grade + grade_2.grade + grade_3.grade) / 3

        Logger.step("### Step 4. Get the stats")
        stats = university_service.get_grades_stats(group_id=group.id)

        Logger.step("### Step 5. Check a business logic")
        assert stats.avg == expected_avg, (
            f"Wrong calculating, Actual: '{stats.avg}', but expected: '{expected_avg}'"
        )

    def test_count_total_grades(
        self,
        university_api_utils_admin,
        student_factory,
        teacher_factory,
        group_factory,
        grade_factory,
    ):
        Logger.step("### Step 1. Prepare a group, teacher, and student")
        university_service = UniversityService(api_utils=university_api_utils_admin)
        group = group_factory()
        teacher = teacher_factory()
        student = student_factory(group_id=group.id)

        Logger.step("### Step 2. Give exact grades for check the calculation")
        grade_1 = grade_factory(teacher_id=teacher.id, student_id=student.id, grade=3)
        grade_2 = grade_factory(teacher_id=teacher.id, student_id=student.id, grade=4)
        grade_3 = grade_factory(teacher_id=teacher.id, student_id=student.id, grade=5)

        Logger.step("### Step 3. Set an expected count of grades")
        expected_count = 3

        Logger.step("### Step 4. Get the stats")
        stats = university_service.get_grades_stats(group_id=group.id)

        Logger.step("### Step 5. Check a business logic")
        assert stats.count == expected_count, (
            f"Wrong count of grades, Actual: '{stats.count}', but expected: '{expected_count}'"
        )
