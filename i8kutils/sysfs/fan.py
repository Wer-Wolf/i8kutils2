#!/usr/bin/python3

"""Fan based on the thermal sysfs interface"""

from __future__ import annotations
from contextlib import AbstractContextManager
from typing import BinaryIO, Final, Generator, Literal, Self
from io import FileIO
from os import scandir

SYSFS_THERMAL_PATH: Final[str] = "/sys/class/thermal"
COOLING_DEVICE_PREFIX: Final[str] = "dell-smm-fan"


class Fan(AbstractContextManager['Fan']):
    """Fan using the thermal sysfs interface"""

    state_file: BinaryIO
    max_state: int
    index: int

    __slots__ = (
        "state_file",
        "max_state",
        "index",
    )

    @classmethod
    def from_cooling_device(cls, device_path: str) -> Self:
        """Create Fan from sysfs cooling device"""
        with open(device_path + "/type", encoding="ascii") as file:
            device_type = file.read()

        if not device_type.startswith(COOLING_DEVICE_PREFIX):
            raise ValueError("Invalid cooling device type: " + device_type)

        with open(device_path + "/max_state", encoding="ascii") as file:
            max_state = int(file.read())

        return cls(
            FileIO(device_path + "/cur_state", "r+"),
            max_state,
            int(device_type.removeprefix(COOLING_DEVICE_PREFIX))
        )

    @classmethod
    def from_thermal_sysfs(cls) -> Generator[Self, None, None]:
        """Retrieve available fans from thermal sysfs"""
        with scandir(SYSFS_THERMAL_PATH) as entries:
            for entry in entries:
                try:
                    yield cls.from_cooling_device(entry.path)
                except ValueError:
                    continue

    def __init__(self, state_file: BinaryIO, max_state: int, index: int):
        self.state_file = state_file
        self.max_state = max_state
        self.index = index

    def __exit__(self, *exc: object) -> Literal[False]:
        self.state_file.close()

        return False

    def get_cooling_state(self) -> int:
        """Get cooling state"""
        self.state_file.seek(0)

        return int(self.state_file.read())

    def set_cooling_state(self, state: int) -> None:
        """Set cooling state"""
        if state > self.max_state:
            raise ValueError(f"Cooling state {state} exceeds max. cooling state {self.max_state}")

        self.state_file.write(str(state).encode("ascii"))
