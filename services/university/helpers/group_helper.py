import requests

from services.general.helpers.base_helper import BaseHelper


class GroupHelper(BaseHelper):
    ENDPOINT_PREFIX = "/groups"
    ROOT_ENDPOINT = f"{ENDPOINT_PREFIX}/"

    def post_group(self, json: dict) -> requests.Response:
        response = self.api_utils.post(self.ROOT_ENDPOINT, json=json)
        return response

    def get_groups(self) -> requests.Response:
        response = self.api_utils.get(self.ROOT_ENDPOINT)
        return response

    def get_group_id(self, group_id: int) -> requests.Response:
        GROUP_ID_ENDPOINT = f"{self.ENDPOINT_PREFIX}/{group_id}/"
        response = self.api_utils.get(GROUP_ID_ENDPOINT)
        return response

    def delete_group(self, group_id: int) -> requests.Response:
        GROUP_ID_ENDPOINT = f"{self.ENDPOINT_PREFIX}/{group_id}/"
        response = self.api_utils.delete(GROUP_ID_ENDPOINT)
        return response

    def put_group(self, group_id: int, json: dict) -> requests.Response:
        GROUP_ID_ENDPOINT = f"{self.ENDPOINT_PREFIX}/{group_id}/"
        response = self.api_utils.put(GROUP_ID_ENDPOINT, json=json)
        return response
