i8kutils
========

Overview
========

i8kutils is a collection of utilities for controlling the fans on some Dell
laptops. The utilities are entirely built upon the `dell-smm-hwmon` kernel
module.

The i8kutils package includes the following utilities:

* i8kctl, a command-line utility for interfacing with the kernel module.
* i8kmon, a temperature monitor with fan control capability.

Since 2011 (kernel version 3.0), the kernel module exports temperature and
fan data over the standard linux hwmon interface. If you are running a recent
enough kernel, you might want to take a look at the [lm-sensors project](https://github.com/lm-sensors/lm-sensors).

License
=======

This software is released under the terms of the GNU General Public
Licence version 2 or later:

> Copyright (C) 2001-2009 Massimo Dal Zotto <dz@debian.org>
>
> This program is free software; you can redistribute it and/or modify
> it under the terms of the GNU General Public License as published by
> the Free Software Foundation; either version 2 of the License, or
> (at your option) any later version.
>
> This program is distributed in the hope that it will be useful,
> but WITHOUT ANY WARRANTY; without even the implied warranty of
> MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
> GNU General Public License for more details.
>
> You should have received a copy of the GNU General Public License
> along with this program; if not, write to the Free Software Foundation,
> Inc., 51 Franklin St, Fifth Floor, Boston, MA 02110-1301, USA.

Linux kernel module
===================

The full documentation of the `dell_smm_hwmon` kernel module can be found
[here](https://docs.kernel.org/hwmon/dell-smm-hwmon.html).

The following module parameters are worth mentioning:

* ignore_dmi=1
    * forces the driver to load on unknown hardware

* force=1
    * forces the driver to load on unsupported/buggy hardware
    * **might cause problems since it also disables all blacklists
      for buggy hardware, use only when `ignore_dmi=1` is not enough**

* fan_mult=<int>
    * overrides the fan speed multiplicator

* fan_max=<int>
    * overrides the maximum fan state

You can specify the module parameters when loading the module or as kernel
parameter when booting the kernel if the driver is builtin.

To have the module loaded automatically at boot you must manually add the
line "dell-smm-hwmon" into the file /etc/modules or use the modconf utility.
For example:

    $ cat /etc/modules
    # /etc/modules: kernel modules to load at boot time.
    #
    # This file contains the names of kernel modules that should be loaded
    # at boot time, one per line. Lines beginning with "#" are ignored.
    dell-smm-hwmon

Any module parameters must be specified in /etc/modprobe.d/dell-smm-hwmon.conf.
To force dell-smm-hwmon to load on unknown/unsupported hardware, it should contain
the following line:

    options dell-smm-hwmon force=1

i8kctl
======

The `i8kctl` utility provides a command-line interface to the `dell-smm-hwmon` kernel driver.
It only supports a subset of the available sensors, use the `sensors` program to retrieve
all sensor data.

In order to modify fan speeds, the utility requires root privileges.

i8kmon
======

The `i8mon` utility provides a daemon for fan control based on the current temperature.
It can be configured by editing `/etc/i8kmon.conf` and is targeted towards machines
which do not provide adequate BIOS fan control.

The daemon requires root privileges.

Requirements
============

Python >= 3.9 and the `dbus-next` package is required for the utilities to work.

Installation
============

```sh
python3 -m pip install i8kutils
```

Contributors
============

Contributors are listed here, in alphabetical order.

* Pablo Bianucci <pbian@physics.utexas.edu>
    * support for /proc/acpi

* David Bustos <bustos@caltech.edu>
    * patches for generating keyboard events

* Jonathan Buzzard <jonathan@buzzard.org.uk>
    * basic information on the SMM BIOS and the Toshiba SMM driver
    * Asm code for calling the SMM BIOS on the I8K. Without his help
      this work wouldn't have been possible.

* Karl E. Jørgensen <karl@jorgensen.com>
    * init script for i8kmon daemon

* Stephane Jourdois <stephane@tuxfinder.org>
    * patches for correctly interpreting buttons status in the i8k driver

* Marcel J.E. Mol <marcel@mesa.nl>
    * patches for the --repeat option in the i8kbuttons (obsolete on Abr 30, 2014) util

* Gianni Tedesco <gianni@ecsc.co.uk>
    * patch to restrict fan contol to SYS_ADMIN capability

* David Woodhouse <dwmw2@redhat.com>
    * suggestions on how to avoid the zombies in i8kbuttons (obsolete on Abr 30, 2014)

* Vitor Augusto <vitorafsr@gmail.com>
    * fixes for the freeze bug at i8kmon, general update and bug fixes

and many others who tested the driver on their hardware and sent reports
and patches.

No credits to DELL Computer who has always refused to provide documentation regarding
the low level BIOS interface used by the kernel module.

---
Massimo Dal Zotto <dz@debian.org>
