import requests

from helper.base_helper import BaseHelper


class StudentHelper(BaseHelper):
    ENDPOINT_PREFIX = "/students"
    ROOT_ENDPOINT = f"{ENDPOINT_PREFIX}/"

    def post_student(self, json: dict) -> requests.Response:
        response = self.api_utils.post(self.ROOT_ENDPOINT, json=json)
        return response

    # def get_student(self) -> requests.Response:
    #     response = self.api_utils.get(self.ROOT_ENDPOINT)
    #     return response
