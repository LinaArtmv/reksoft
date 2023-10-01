import json
from decimal import Decimal
from urllib.parse import parse_qs


class Request:

    def __init__(self, environ: dict):
        self.build_get_params_dict(environ['PATH_INFO'])
        self.build_get_query_params_dict(environ['RAW_URI'])
        self.build_post_params_dict(environ['wsgi.input'].read())
        self.build_delete_params_dict(environ['wsgi.input'].read())
        self.environ = environ
        self.extra = {}

    def __getattr__(self, item):
        return self.extra[item] if item in self.extra else None

    def build_get_params_dict(self, raw_params: str):
        if len(raw_params.split('/')) > 2:
            id = raw_params.split('/')[2]
            self.GET = {'id': id}
        else:
            params = parse_qs(raw_params)
            self.GET = params

    def build_get_query_params_dict(self, raw_params: str):
        params = {}
        try:
            parts = raw_params.split('=')
            if len(parts) < 2:
                self.GET_QUERY = params
            value = parts[1]
            if '/' in value:
                value_parts = value.split('/')
                digit = value_parts[0]
                if digit.isdigit():
                    self.GET_QUERY = {'type': digit}
        except Exception:
            self.GET_QUERY = params

    def build_post_params_dict(self, raw_bytes: bytes):
        raw_params = raw_bytes.decode('utf-8')
        try:
            json_data = json.loads(raw_params, parse_float=Decimal)
            self.POST = json_data
        except json.JSONDecodeError:
            self.POST = parse_qs(raw_params)

    def build_delete_params_dict(self, raw_bytes: bytes):
        raw_params = raw_bytes.decode('utf-8')
        try:
            json_data = json.loads(raw_params)
            self.DELETE = json_data
        except json.JSONDecodeError:
            self.DELETE = parse_qs(raw_params)
