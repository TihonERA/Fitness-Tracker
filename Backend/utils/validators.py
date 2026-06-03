class NotFound(Exception):
    def __init__(self, detail: str = "Not Found"):
        self.status_code = 404
        self.detail = detail
        super().__init__(detail)