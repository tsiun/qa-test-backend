from faker import Faker


from logger.logger import Logger


faker = Faker()


class TestGradeCreate:
    def test_create_grade_admin(self, grade_data):
        Logger.step("Check that the grade is created by admin")

        assert grade_data.id is not None, (
            f"The grade wasn't given, Actual: 'None', but expected: '{grade_data.id}' "
        )

    def test_create_grade_by_teacher(self, grade_data, teacher_data):
        Logger.step("Check that the grade is created by teacher")

        assert grade_data.teacher_id == teacher_data.id, (
            f"Wrong teacher id, Actual: '{grade_data.teacher_id}', but expected: '{teacher_data.id}'"
        )

    def test_create_grade_to_student(self, grade_data, student_data):
        Logger.step("Check that the grade is given to the student")

        assert grade_data.student_id == student_data.id, (
            f"Wrong student id, Actual: '{grade_data.student_id}', but expected: '{student_data.id}'"
        )
