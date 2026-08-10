import requests

from services.general.helpers.base_helper import BaseHelper


class TeacherHelper(BaseHelper):
    ENDPOINT_PREFIX = "/teachers"
    ROOT_ENDPOINT = f"{ENDPOINT_PREFIX}/"

    def post_teacher(self, json: dict) -> requests.Response:
        response = self.api_utils.post(self.ROOT_ENDPOINT, json=json)
        return response

    def get_teachers(self) -> requests.Response:
        response = self.api_utils.get(self.ROOT_ENDPOINT)
        return response

    def get_teacher(self, teacher_id: int) -> requests.Response:
        TEACHER_ID_ENDPOINT = f"{self.ENDPOINT_PREFIX}/{teacher_id}/"
        response = self.api_utils.get(TEACHER_ID_ENDPOINT)
        return response

    def delete_teacher(self, teacher_id: int) -> requests.Response:
        TEACHER_ID_ENDPOINT = f"{self.ENDPOINT_PREFIX}/{teacher_id}/"
        response = self.api_utils.delete(TEACHER_ID_ENDPOINT)
        return response

    def put_teacher(self, teacher_id: int, json: dict) -> requests.Response:
        TEACHER_ID_ENDPOINT = f"{self.ENDPOINT_PREFIX}/{teacher_id}/"
        response = self.api_utils.put(TEACHER_ID_ENDPOINT, json=json)
        return response
