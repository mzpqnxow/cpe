# -*- coding: utf-8 -*-


class Cpe1_1(object):

    def __init__(self, cpe_name):
        self.name = cpe_name
        self._parse_name()

    def _parse_name(self):
        part_list = self.name.split("/")
        hardware_component_list = part_list[1].split(":")
        component_key_list = ["vendor", "product", "version"]
        hardware_element = {}

        for i in range(0, len(hardware_component_list)):
            hardware_element[component_key_list[i]] = hardware_component_list[i]

        self.prefix = part_list[0]
        self.hardware_part = [hardware_element]

    def as_dict(self):
        return {
            "prefix": self.prefix,
            "hardware": self.hardware_part,
        }

    def get_hardware_part(self):
        return []

    def get_os_part(self):
        return []

    def get_application_part(self):
        return []
