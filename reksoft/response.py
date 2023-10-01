import json
from decimal import Decimal


class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return str(obj)
        return super().default(obj)


class Response:

    def __init__(self, request,
                 status_code: int = 200,
                 headers: dict = None,
                 body: str = ''):
        self.status_code = status_code
        self.headers = {}
        self.body = {}
        self._set_base_headers()
        if headers is not None:
            self.update_headers(headers)
        self._set_body(body)
        self.request = request
        self.extra = {}

    def __getattr__(self, item):
        return self.extra.get(item)

    def _set_base_headers(self):
        self.headers = {
            "Content-Type": "application/json",
            "Content-Length": 0
        }

    def _set_body(self, raw_json):
        self.body = json.dumps(raw_json, cls=DecimalEncoder).encode('utf-8')
        self.update_headers(
            {"Content-Length": str(len(self.body))}
        )

    def update_headers(self, headers: dict):
        self.headers.update(headers)
