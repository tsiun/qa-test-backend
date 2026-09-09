import requests

from services.general.helpers.base_helper import BaseHelper


class GroupHelper(BaseHelper):
    ENDPOINT_PREFIX = "/groups"
    ROOT_ENDPOINT = f"{ENDPOINT_PREFIX}/"
    GROUP_ID_ENDPOINT = f"{ENDPOINT_PREFIX}/{{group_id}}/"

    def post_group(self, json: dict) -> requests.Response:
        response = self.api_utils.post(self.ROOT_ENDPOINT, json=json)
        return response

    def get_groups(self) -> requests.Response:
        response = self.api_utils.get(self.ROOT_ENDPOINT)
        return response

    def get_group(self, group_id: int) -> requests.Response:
        group_id_endpoint = f"{self.ENDPOINT_PREFIX}/{group_id}/"
        response = self.api_utils.get(group_id_endpoint)
        return response

    def delete_group(self, group_id: int) -> requests.Response:
        group_id_endpoint = self.GROUP_ID_ENDPOINT.format(group_id=group_id)
        response = self.api_utils.delete(group_id_endpoint)
        return response

    def put_group(self, group_id: int, json: dict) -> requests.Response:
        group_id_endpoint = self.GROUP_ID_ENDPOINT.format(group_id=group_id)
        response = self.api_utils.put(group_id_endpoint, json=json)
        return response
