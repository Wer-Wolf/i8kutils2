#!/usr/bin/python3

"""Chip for detecting present fans"""

from typing import Final, Self
import re
import os

SYSFS_HWMON_PATH: Final[str] = "/sys/class/hwmon"
DELL_SMM_HWMON_CHIP_NAME: Final[str] = "dell_smm\n"

REGEX: Final = re.compile(r"fan(\d)_input", re.A)


class HwmonChip:
    """Detects available fans"""

    hwmon_device_path: str

    __slots__ = (
        "hwmon_device_path",
    )

    @classmethod
    def autodetect(cls) -> Self:
        """Autodetect hwmon chip from sysfs"""
        with os.scandir(SYSFS_HWMON_PATH) as entries:
            for entry in filter(lambda e: e.is_dir, entries):
                with open(entry.path + "/name", encoding="ascii") as file:
                    chip_name = file.read()

                if chip_name == DELL_SMM_HWMON_CHIP_NAME:
                    return cls(entry.path)

        raise RuntimeError("Unable to find hwmon chip")

    def __init__(self, hwmon_device_path: str) -> None:
        self.hwmon_device_path = hwmon_device_path

    def fans(self) -> int:
        """Detect number of fans"""
        results = filter(REGEX.fullmatch, os.listdir(self.hwmon_device_path))

        return sum(1 for _ in results)
