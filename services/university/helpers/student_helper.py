import requests

from services.general.helpers.base_helper import BaseHelper


class StudentHelper(BaseHelper):
    ENDPOINT_PREFIX = "/students"
    ROOT_ENDPOINT = f"{ENDPOINT_PREFIX}/"
    STUDENT_ID_ENDPOINT = f"{ENDPOINT_PREFIX}/{{student_id}}/"

    def post_student(self, json: dict) -> requests.Response:
        response = self.api_utils.post(self.ROOT_ENDPOINT, json=json)
        return response

    def get_students(self) -> requests.Response:
        response = self.api_utils.get(self.ROOT_ENDPOINT)
        return response

    def get_student(self, student_id: int) -> requests.Response:
        student_id_endpoint = self.STUDENT_ID_ENDPOINT.format(student_id=student_id)
        response = self.api_utils.get(student_id_endpoint)
        return response

    def delete_student(self, student_id: int) -> requests.Response:
        student_id_endpoint = self.STUDENT_ID_ENDPOINT.format(student_id=student_id)
        response = self.api_utils.delete(student_id_endpoint)
        return response

    def put_student(self, student_id: int, json: dict) -> requests.Response:
        student_id_endpoint = self.STUDENT_ID_ENDPOINT.format(student_id=student_id)
        response = self.api_utils.put(student_id_endpoint, json=json)
        return response
