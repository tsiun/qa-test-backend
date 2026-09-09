from logger.logger import Logger
from services.university.university_service import UniversityService


class TestGradeDelete:
    def test_grade_delete_admin(
        self,
        university_api_utils_admin,
        teacher_factory,
        student_factory,
        grade_factory,
        group_factory,
    ):
        Logger.step("### Step 1. Prepare data for creating a grade")
        university_service = UniversityService(api_utils=university_api_utils_admin)

        group = group_factory()
        teacher = teacher_factory()
        student = student_factory(group_id=group.id)

        group_id = group.id
        teacher_id = teacher.id
        student_id = student.id

        Logger.step("### Step 2. Creating the grades")
        grade = grade_factory(teacher_id=teacher_id, student_id=student_id, grade=5)

        Logger.step("### Step 3. Deleting the grades")
        university_service.delete_grade(grade_id=grade.id)

        Logger.step("### Step 4. Verify grade deletion")
        result_1 = university_service.get_grades(
            student_id=student_id, teacher_id=teacher_id, group_id=group_id
        )

        assert result_1 == [], (
            f"The grade was not deleted, Actual result:'{result_1}', but expected: '{[]}'"
        )
