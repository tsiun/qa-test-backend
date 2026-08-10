import requests

from services.general.helpers.base_helper import BaseHelper


class StudentHelper(BaseHelper):
    ENDPOINT_PREFIX = "/students"
    ROOT_ENDPOINT = f"{ENDPOINT_PREFIX}/"
    # STUDENT_ID_ENDPOINT = f"{ENDPOINT_PREFIX}/{student_id}/"

    def post_student(self, json: dict) -> requests.Response:
        response = self.api_utils.post(self.ROOT_ENDPOINT, json=json)
        return response

    def get_students(self) -> requests.Response:
        response = self.api_utils.get(self.ROOT_ENDPOINT)
        return response

    def get_student(self, student_id: int) -> requests.Response:
        STUDENT_ID_ENDPOINT = f"{self.ENDPOINT_PREFIX}/{student_id}/"
        response = self.api_utils.get(STUDENT_ID_ENDPOINT)
        return response

    def delete_student(self, student_id: int) -> requests.Response:
        STUDENT_ID_ENDPOINT = f"{self.ENDPOINT_PREFIX}/{student_id}/"
        response = self.api_utils.delete(STUDENT_ID_ENDPOINT)
        return response

    def put_student(self, student_id: int, json: dict) -> requests.Response:
        STUDENT_ID_ENDPOINT = f"{self.ENDPOINT_PREFIX}/{student_id}/"
        response = self.api_utils.put(STUDENT_ID_ENDPOINT, json=json)
        return response
