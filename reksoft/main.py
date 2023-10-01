import re
from typing import List

from reksoft.exceptions import NotAllowed, NotFound
from reksoft.request import Request
from reksoft.response import Response
from reksoft.urls import Url
from reksoft.view import View


class Resource:

    __slots__ = ('urls',)

    def __init__(self, urls: List[Url]):
        self.urls = urls

    def __call__(self, environ: dict, start_response, **kwargs):
        view = self._get_view(environ)
        request = self._get_request(environ)
        response = self._get_response(environ, view, request)
        start_response(str(response.status_code), response.headers.items())
        return iter([response.body])

    def _get_view(self, environ: dict) -> View:
        raw_url = str(environ["PATH_INFO"])
        view = self._find_view(raw_url)('reksoft')
        return view

    def _get_request(self, environ: dict) -> Request:
        return Request(environ)

    def _get_response(self, environ: dict,
                      view: View, request: Request) -> Response:
        method = environ["REQUEST_METHOD"].lower()
        if not hasattr(view, method):
            raise NotAllowed
        return getattr(view, method)(request)

    def _prepare_url(self, url: str):
        """Удаляем краевой /"""

        if url[-1] == '/':
            return url[:-1]
        return url

    def _find_view(self, raw_url: str):
        """Найти view или отдать ошибку 404"""

        url = self._prepare_url(raw_url)
        for path in self.urls:
            m = re.match(path.url, url)
            if m is not None:
                return path.view
        raise NotFound
