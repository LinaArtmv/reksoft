from dataclasses import dataclass
from typing import Type

from reksoft.view import View


@dataclass
class Url:
    url: str
    view: Type[View]
