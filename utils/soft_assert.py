class SoftAssert:
    def __init__(self):
        self.errors: list[str] = []

    def check(self, condition: bool, message: str):
        if not condition:
            self.errors.append(message)

    def assert_all(self):
        if self.errors:
            summary = "\n".join(f"{i}: {err}" for i, err in enumerate(self.errors, 1))
            raise AssertionError(f"Found {len(self.errors)} errors: \n{summary}")
