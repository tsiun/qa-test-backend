import requests

from services.general.helpers.base_helper import BaseHelper


class GradeHelper(BaseHelper):
    ENDPOINT_PREFIX = "/grades"
    ROOT_ENDPOINT = f"{ENDPOINT_PREFIX}/"
    GRADE_STATS_ENDPOINT = f"{ENDPOINT_PREFIX}/stats/"

    def post_grade(self, json: dict) -> requests.Response:
        response = self.api_utils.post(self.ROOT_ENDPOINT, json=json)
        return response

    def get_grades(self) -> requests.Response:
        response = self.api_utils.get(self.ROOT_ENDPOINT)
        return response

    def get_grades_stats(self) -> requests.Response:
        response = self.api_utils.get(self.GRADE_STATS_ENDPOINT)
        return response

    def delete_grade(self, grade_id: int) -> requests.Response:
        GRADE_ID_ENDPOINT = f"{self.ENDPOINT_PREFIX}/{grade_id}/"
        response = self.api_utils.delete(GRADE_ID_ENDPOINT)
        return response

    def put_grade(self, grade_id: int, json: dict) -> requests.Response:
        GRADE_ID_ENDPOINT = f"{self.ENDPOINT_PREFIX}/{grade_id}/"
        response = self.api_utils.put(GRADE_ID_ENDPOINT, json=json)
        return response
