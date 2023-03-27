#!/usr/bin/python3

"""Config file parser"""

from __future__ import annotations
from dataclasses import dataclass
from tkinter import Tcl, TclError
from typing import Final, Self

DEFAULT_CONFIG_PATH: Final[str] = "/etc/i8kmon.conf"


@dataclass(frozen=True, slots=True)
class FanControlConfig:
    """Fan control configuration"""

    update_period: int

    ondemand: bool

    verbose: bool

    states: list[FanStateConfig]

    @classmethod
    def from_config_file(cls, config_path: str) -> Self:
        """Parse fan configuration from file"""
        tcl = Tcl()
        state_configs = list()

        with open(config_path, encoding="utf-8") as file:
            config = file.read()

        tcl.eval(config)
        try:
            update_period = int(tcl.getvar("config(timeout)"))
        except TclError:
            update_period = 1

        try:
            if int(tcl.getvar("config(ondemand)")) > 0:
                ondemand = True
            else:
                ondemand = False
        except TclError:
            ondemand = False

        try:
            if int(tcl.getvar("config(verbose)")) > 0:
                verbose = True
            else:
                verbose = False
        except TclError:
            verbose = False

        try:
            num_configs = int(tcl.getvar("config(num_configs)"))

            for i in range(num_configs):
                fan_config = dict()
                states: list[str] = tcl.eval(f"lindex $config({i}) 0").split()
                low_treshold_ac = int(tcl.eval(f"lindex $config({i}) 1"))
                high_treshold_ac = int(tcl.eval(f"lindex $config({i}) 2"))
                low_treshold_battery = int(tcl.eval(f"lindex $config({i}) 3"))
                high_treshold_battery = int(tcl.eval(f"lindex $config({i}) 4"))

                states.reverse()
                for index, state in enumerate(states, start=1):
                    if state == '-':
                        continue

                    fan_config[index] = int(state)

                state_config = FanStateConfig(fan_config, low_treshold_ac, high_treshold_ac, low_treshold_battery, high_treshold_battery)
                state_configs.append(state_config)
        except TclError:
            pass    # TODO

        del tcl

        return cls(update_period, ondemand, verbose, state_configs)


@dataclass(frozen=True, slots=True)
class FanStateConfig:
    """Fan state configuration"""

    fan_config: dict[int, int]

    low_treshold_ac: int

    high_treshold_ac: int

    low_treshold_battery: int

    high_treshold_battery: int
