#!/usr/bin/python3

"""Fan control session handling"""
from __future__ import annotations
from contextlib import AbstractContextManager
from typing import Literal, Self

from .controller import FanController


class FanControlSession(AbstractContextManager['FanControlSession']):
    """Fan control session handling"""

    controller: FanController

    __slots__ = (
        "controller",
    )

    def __init__(self, controller: FanController) -> None:
        self.controller = controller

    def __enter__(self) -> Self:
        self.controller.enable()

        return self

    def __exit__(self, *exc: object) -> Literal[False]:
        self.controller.disable()

        return False
