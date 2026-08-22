class TestGroupCreate:
    def test_create_group_by_admin(self, group_data):
        assert group_data.id is not None, (
            f"The group wasn't create, Actual: 'None', but expected: '{group_data.id}'"
        )
