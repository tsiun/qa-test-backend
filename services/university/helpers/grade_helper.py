import requests

from services.general.helpers.base_helper import BaseHelper


class GradeHelper(BaseHelper):
    ENDPOINT_PREFIX = "/grades"
    ROOT_ENDPOINT = f"{ENDPOINT_PREFIX}/"
    GRADE_STATS_ENDPOINT = f"{ENDPOINT_PREFIX}/stats/"
    GRADE_ID_ENDPOINT = f"{ENDPOINT_PREFIX}/{{grade_id}}/"

    def post_grade(self, data: dict) -> requests.Response:
        response = self.api_utils.post(self.ROOT_ENDPOINT, data=data)
        return response

    def get_grades(self, params: dict | None = None) -> requests.Response:
        response = self.api_utils.get(self.ROOT_ENDPOINT, params=params)
        return response

    def get_grades_stats(self, params: dict | None = None) -> requests.Response:
        response = self.api_utils.get(self.GRADE_STATS_ENDPOINT, params=params)
        return response

    def delete_grade(self, grade_id: int) -> requests.Response:
        grade_id_endpoint = self.GRADE_ID_ENDPOINT.format(grade_id=grade_id)
        response = self.api_utils.delete(grade_id_endpoint)
        return response

    def put_grade(self, grade_id: int, data: dict) -> requests.Response:
        grade_id_endpoint = self.GRADE_ID_ENDPOINT.format(grade_id=grade_id)
        response = self.api_utils.put(grade_id_endpoint, data=data)
        return response
