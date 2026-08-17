import requests

from services.general.helpers.base_helper import BaseHelper


class GradeHelper(BaseHelper):
    ENDPOINT_PREFIX = "/grades"
    ROOT_ENDPOINT = f"{ENDPOINT_PREFIX}/"
    GRADE_STATS_ENDPOINT = f"{ENDPOINT_PREFIX}/stats/"
    GRADE_ID_ENDPOINT = f"{ENDPOINT_PREFIX}/{{grade_id}}/"

    def post_grade(self, json: dict) -> requests.Response:
        response = self.api_utils.post(self.ROOT_ENDPOINT, json=json)
        return response

    def get_grades(self, params: dict | None = None) -> requests.Response:
        response = self.api_utils.get(self.ROOT_ENDPOINT)
        return response

    def get_grades_stats(
            self,
            teacher_id: int | None = None,
            student_id: int | None = None,
            group_id: int | None = None,
    ) -> requests.Response:
        params = {
            "teacher_id": teacher_id,
            "student_id": student_id,
            "group_id": group_id,
        }
        params = {k: v for k, v in params.items() if v is not None}
        response = self.api_utils.get(self.GRADE_STATS_ENDPOINT, **params)
        return response

    def delete_grade(self, grade_id: int) -> requests.Response:
        grade_id_endpoint = self.GRADE_ID_ENDPOINT.format(grade_id=grade_id)
        response = self.api_utils.delete(grade_id_endpoint)
        return response

    def put_grade(self, grade_id: int, json: dict) -> requests.Response:
        grade_id_endpoint = self.GRADE_ID_ENDPOINT.format(grade_id=grade_id)
        response = self.api_utils.put(grade_id_endpoint, json=json)
        return response
