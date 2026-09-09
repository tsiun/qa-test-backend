import requests

from services.general.helpers.base_helper import BaseHelper


class TeacherHelper(BaseHelper):
    ENDPOINT_PREFIX = "/teachers"
    ROOT_ENDPOINT = f"{ENDPOINT_PREFIX}/"
    TEACHER_ID_ENDPOINT = f"{ENDPOINT_PREFIX}/{{teacher_id}}/"

    def post_teacher(self, json: dict) -> requests.Response:
        response = self.api_utils.post(self.ROOT_ENDPOINT, json=json)
        return response

    def get_teachers(self) -> requests.Response:
        response = self.api_utils.get(self.ROOT_ENDPOINT)
        return response

    def get_teacher(self, teacher_id: int) -> requests.Response:
        teacher_id_endpoint = self.TEACHER_ID_ENDPOINT.format(teacher_id=teacher_id)
        response = self.api_utils.get(teacher_id_endpoint)
        return response

    def delete_teacher(self, teacher_id: int) -> requests.Response:
        teacher_id_endpoint = self.TEACHER_ID_ENDPOINT.format(teacher_id=teacher_id)
        response = self.api_utils.delete(teacher_id_endpoint)
        return response

    def put_teacher(self, teacher_id: int, json: dict) -> requests.Response:
        teacher_id_endpoint = self.TEACHER_ID_ENDPOINT.format(teacher_id=teacher_id)
        response = self.api_utils.put(teacher_id_endpoint, json=json)
        return response
