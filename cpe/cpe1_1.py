# -*- coding: utf-8 -*-

from .part import CpePart


class Cpe1_1(object):
    def __init__(self, cpe_name):
        self.name = cpe_name
        self._parse_name()
        self.version = "1.1"
        self.part_list = None

    def _parse_name(self):
        part_list = self.name.split("/")

        self.prefix = part_list[0]
        self.hardware_part = []
        self.os_part = []
        self.application_part = []

        part_list = part_list[1:]

        for p in range(0, len(part_list)):

            if p == 0:
                part = CpePart(part_list[p], "hardware")
                self.hardware_part = part.element_list
            elif p == 1:
                part = CpePart(part_list[p], "os")
                self.os_part = part.element_list
            elif p == 2:
                part = CpePart(part_list[p], "application")
                self.application_part = part.element_list
            else:
                raise ValueError("CPE Name with more than three parts")

    def as_dict(self):
        return {
            "prefix": self.prefix,
            "hardware": self.hardware_part,
            "os": self.os_part,
            "application": self.application_part,
        }

    def get_hardware_part(self):
        return self.hardware_part

    def get_os_part(self):
        return self.os_part

    def get_application_part(self):
        return self.application_part
