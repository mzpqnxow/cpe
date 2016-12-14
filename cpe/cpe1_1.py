# -*- coding: utf-8 -*-


class Cpe1_1(object):

    def __init__(self, cpe_name):
        self.name = cpe_name
        self._parse_name()

    @staticmethod
    def _parse_part(part_data):
        element_list = []
        component_key_list = ["vendor", "product", "version"]

        for elem in part_data.split(";"):
            component_list = elem.split(":")
            element = {}

            for i in range(0, len(component_list)):
                element[component_key_list[i]] = component_list[i]

            element_list.append(element)
        return element_list

    def _parse_name(self):
        part_list = self.name.split("/")

        self.prefix = part_list[0]
        self.hardware_part = []
        self.os_part = []
        self.application_part = []

        part_list = part_list[1:]

        for p in range(0, len(part_list)):
            part = part_list[p]
            parsed_part = []

            if len(part) > 0:
                parsed_part = self._parse_part(part)

            if p == 0:
                self.hardware_part = parsed_part
            elif p == 1:
                self.os_part = parsed_part
            elif p == 2:
                self.application_part = parsed_part
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
