#!/usr/bin/python3

"""Fan controller for fan mode control"""
from __future__ import annotations
from contextlib import AbstractContextManager
from typing import BinaryIO, Final, Literal, Self
from io import FileIO
import stat
import os

FAN_CONTROL_ATTR: Final[str] = "pwm1_enable"


class FanController(AbstractContextManager['FanController']):
    """Fan controller using the hwmon sysfs interface"""

    enable_file: BinaryIO

    __slots__ = (
        "enable_file",
    )

    @classmethod
    def from_hwmon_device(cls, device_path: str) -> Self:
        """Create FanController from hwmon device"""
        path = f"{device_path}/{FAN_CONTROL_ATTR}"
        mode = os.stat(path)

        if stat.S_IMODE(mode.st_mode) != 0o200:
            raise RuntimeError("Fan control method not supported")

        return cls(FileIO(path, "w"))

    def __init__(self, file: BinaryIO) -> None:
        self.enable_file = file

    def __exit__(self, *exc: object) -> Literal[False]:
        self.enable_file.close()

        return False

    def enable(self) -> None:
        """Enable manual fan control"""
        self.enable_file.write("1".encode("ascii"))

    def disable(self) -> None:
        """Disable manual fan control"""
        self.enable_file.write("2".encode("ascii"))
