#! /usr/bin/env python
# Copyright (c) 2018 - 2019 Jolle Jolles <j.w.jolles@gmail.com>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at:
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import print_function

import io
import os
import re
import sys
import socket
import fractions

class Logger(object):
    def __init__(self, filename):
        self.terminal = sys.stdout
        self.log = open(filename, "a")
    def __getattr__(self, attr):
        return getattr(self.terminal, attr)
    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)
    def flush(self):
        pass


def deleteline(n=1):

    for _ in range(n):
        sys.stdout.write('\x1b[1A')
        sys.stdout.write('\x1b[2K')


def lineprint(text, stamp=True, sameline=False, reset=False, **kwargs):

    global line, label

    line = line if vardefined("line") else ""
    label = label if vardefined("label") else socket.gethostname()
    if not vardefined("label"):
        label = ""

    if "label" in kwargs:
        label = kwargs["label"]

    if stamp and not sameline:
        text = time.strftime("%H:%M:%S") + " [" + label + "] - " + text

    if sameline:
        if reset:
            line = text
            sys.stdout.write("\r")
            sys.stdout.write(" "*100)
        else:
            text = line + " " + text
        line = "\r" + text
        print(line,end='')
    else:
        line = text
        if line == "":
            print(line, end=' ')
        else:
            print(text,end="\n")


def hide_traceback():

    """
    Hides traceback in jupyter when raising errors. Only shows error. Only needs
    to be called at start of script.
    """

    ipython = get_ipython()

    def hide(exc_tuple = None, filename = None, tb_offset = None,
             exception_only = False, running_compiled_code = False):
        etype, value, tb = sys.exc_info()
        element = ipython.InteractiveTB.get_exception_only(etype, value)

        return ipython._showtraceback(etype, value, element)

    ipython.showtraceback = hide


def homedir():

    """Returns the home directory"""

    return os.path.expanduser("~")+"/"


def isscript():

    """Determines if session is script or interactive (jupyter)"""

    import __main__ as main
    return hasattr(main, '__file__')


def is_rpi(message=False):

    """Checks if current system is a Raspberry Pi"""

    try:
        with io.open('/proc/cpuinfo', 'r') as cpuinfo:
            found = False
            for line in cpuinfo:
                if line.startswith('Hardware'):
                    found = True
                    label, value = line.strip().split(':', 1)
                    value = value.strip()
                    if value not in ('BCM2708','BCM2709','BCM2835','BCM2836'):
                        return False
            if not found:
                raise ValueError("""Unable to determine if system is rpi or
                                 not. Set system manually""")

    except IOError:
        if message:
            lineprint("non-rpi system detected..")
        return False

    if message:
        lineprint("rpi system detected..")
    return True


def vardefined(var):

    return var in [var for var,_ in globals().items()]


def check_frac(input_txt):

    """Checks string for Fractions and converts them accordingly"""

    transformed_text = re.sub(r'([\d.]+)', r'Fraction("\1")', input_txt)

    return eval(transformed_text)
