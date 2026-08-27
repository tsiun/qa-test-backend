from logger.logger import Logger
from services.university.models.grade_stats_response import GradeStatsResponse
from services.university.university_service import UniversityService


class TestGetStatBusinessLogic:
    def test_average_calculation(
        self,
        university_api_utils_admin,
        common_entities,
    ):
        Logger.step("### Step 1. Get common entities")
        university_service = UniversityService(api_utils=university_api_utils_admin)
        group = common_entities["group"]
        grades = common_entities["grades"]

        Logger.step("### Step 2. Calculate an expected result")
        expected_avg = sum(grade.grade for grade in grades) / len(grades)

        Logger.step("### Step 3. Get the stats")
        stats = university_service.get_grades_stats(group_id=group.id)

        Logger.step("### Step 4. Check a business logic")
        assert stats.avg == expected_avg, (
            f"Wrong calculating, Actual: '{stats.avg}', but expected: '{expected_avg}'"
        )

    def test_count_total_grades(
        self,
        university_api_utils_admin,
        common_entities,
    ):
        Logger.step("### Step 1. Get common entities")
        university_service = UniversityService(api_utils=university_api_utils_admin)
        group = common_entities["group"]
        expected_count = len(common_entities["grades"])

        Logger.step("### Step 2. Get the stats")
        stats = university_service.get_grades_stats(group_id=group.id)

        Logger.step("### Step 3. Check a business logic")
        assert stats.count == expected_count, (
            f"Wrong count of grades, Actual: '{stats.count}', but expected: '{expected_count}'"
        )

    def test_check_grades_when_teachers_overlap(
        self,
        university_api_utils_admin,
        student_factory,
        teacher_factory,
        group_factory,
        grade_factory,
        soft_assert,
    ):
        Logger.step("### Step 1. Prepare a group, teachers, and student")
        university_service = UniversityService(api_utils=university_api_utils_admin)
        group = group_factory()
        teacher_1 = teacher_factory()
        teacher_2 = teacher_factory()
        student_1 = student_factory(group_id=group.id)
        student_2 = student_factory(group_id=group.id)

        Logger.step("### Step 2. Give exact grades for check the calculation")
        grade_1 = grade_factory(
            teacher_id=teacher_1.id, student_id=student_1.id, grade=3
        )
        grade_2 = grade_factory(
            teacher_id=teacher_2.id, student_id=student_2.id, grade=4
        )

        Logger.step("### Step 3. Set an expected count of grades")
        expected_count = 2
        teacher_1_grades = 1

        Logger.step("### Step 4. Get the stats")
        stats_group = university_service.get_grades_stats(group_id=group.id)
        stats_teacher_1 = university_service.get_grades_stats(teacher_id=teacher_1.id)

        Logger.step("### Step 5. Check a business logic")

        soft_assert.check(
            stats_group.count == expected_count,
            f"Wrong count of grades, Actual: '{stats_group.count}', but expected: '{expected_count}'",
        )
        soft_assert.check(
            stats_teacher_1.count == teacher_1_grades,
            f"Wrong count of grades, Actual: '{stats_teacher_1.count}', but expected: '{teacher_1_grades}'",
        )
        soft_assert.assert_all()

    def test_check_avg_after_deleting_one_grade(
        self,
        university_api_utils_admin,
        group_factory,
        student_factory,
        teacher_factory,
        grade_factory,
        soft_assert,
    ):
        Logger.step("### Step 1. Prepare a group, teacher, and student")
        university_service = UniversityService(api_utils=university_api_utils_admin)
        group = group_factory()
        teacher = teacher_factory()
        student_1 = student_factory(group_id=group.id)
        student_2 = student_factory(group_id=group.id)
        student_3 = student_factory(group_id=group.id)

        Logger.step("### Step 2. Give exact grades for check the calculation")
        grade_1 = grade_factory(teacher_id=teacher.id, student_id=student_1.id, grade=3)
        grade_2 = grade_factory(teacher_id=teacher.id, student_id=student_2.id, grade=4)
        grade_3 = grade_factory(teacher_id=teacher.id, student_id=student_3.id, grade=5)

        Logger.step("### Step 3. Calculate an expected result")
        expected_avg_before_delete = (grade_1.grade + grade_2.grade + grade_3.grade) / 3

        Logger.step("### Step 4. Get the stats before deleting a grade")
        stats_before_delete = university_service.get_grades_stats(group_id=group.id)

        Logger.step("### Step 5. Check the first step of business logic")
        soft_assert.check(
            stats_before_delete.avg == expected_avg_before_delete,
            (
                f"Wrong calculating before deleting a grade, Actual: '{stats_before_delete.avg}', but expected: '{expected_avg_before_delete}'"
            ),
        )

        Logger.step("### Step 6. Delete one of the grades")
        university_service.delete_grade(grade_id=grade_1.id)

        Logger.step("### Step 7. Calculate an expected result after deleting a grade")
        expected_avg_after_delete = (grade_2.grade + grade_3.grade) / 2

        Logger.step("### Step 7. Get the stats after deleting a grade")
        stats_after_delete = university_service.get_grades_stats(group_id=group.id)

        Logger.step("### Step 8. Check the second step of business logic")
        soft_assert.check(
            stats_after_delete.avg == expected_avg_after_delete,
            (
                f"Wrong calculating after deleting a grade, Actual: '{stats_after_delete.avg}', but expected: '{expected_avg_after_delete}'"
            ),
        )

        soft_assert.assert_all()

    def test_check_min_and_max_grades(
        self,
        university_api_utils_admin,
        group_factory,
        student_factory,
        teacher_factory,
        grade_factory,
        soft_assert,
    ):
        Logger.step("### Step 1. Prepare a group, teacher, and student")
        university_service = UniversityService(api_utils=university_api_utils_admin)
        group = group_factory()
        teacher = teacher_factory()
        student_1 = student_factory(group_id=group.id)
        student_2 = student_factory(group_id=group.id)
        student_3 = student_factory(group_id=group.id)

        Logger.step("### Step 2. Give exact grades for check the calculation")
        grade_1 = grade_factory(teacher_id=teacher.id, student_id=student_1.id, grade=1)
        grade_2 = grade_factory(teacher_id=teacher.id, student_id=student_2.id, grade=3)
        grade_3 = grade_factory(teacher_id=teacher.id, student_id=student_3.id, grade=5)

        Logger.step("### Step 3. Get the stats of grades")
        stats = university_service.get_grades_stats(group_id=group.id)
        min_grade = stats.min
        max_grade = stats.max

        Logger.step("### Step 4. Check the min grade")
        soft_assert.check(
            min_grade == 1,
            (
                f"Wrong definition of min grade, Actual: '{min_grade}', but expected: '1'"
            ),
        )

        Logger.step("### Step 5. Check the max grade")
        soft_assert.check(
            max_grade == 5,
            (
                f"Wrong definition of max grade, Actual: '{max_grade}', but expected: '5'"
            ),
        )

        soft_assert.assert_all()

    def test_count_avg_grade_in_empty_group(
        self,
        university_api_utils_admin,
        group_factory,
    ):
        Logger.step("### Step 1. Prepare a group")
        university_service = UniversityService(api_utils=university_api_utils_admin)
        group = group_factory()

        Logger.step("### Step 2. Get the stats")
        stats = university_service.get_grades_stats(group_id=group.id)

        Logger.step("### Step 3. Create an expected result")
        expected_status = GradeStatsResponse(
            count=0,
            min=None,
            max=None,
            avg=None,
        )

        Logger.step("### Step 3. Check a business logic")
        assert stats == expected_status, (
            f"Wrong calculating in empty group, Actual: '{stats}', but expected: '{expected_status}'"
        )
