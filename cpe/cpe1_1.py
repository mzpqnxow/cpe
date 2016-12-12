# -*- coding: utf-8 -*-


class Cpe1_1(object):

    def __init__(self, cpe_name):
        self.name = cpe_name
        self._parse_name()

    def _parse_name(self):
        part_list = self.name.split("/")

        if len(part_list[1]) == 0:
            self.hardware_part = []
        else:
            hw_element_list = []

            for elem in part_list[1].split(";"):
                hw_component_list = elem.split(":")
                component_key_list = ["vendor", "product", "version"]
                hw_element = {}

                for i in range(0, len(hw_component_list)):
                    hw_element[component_key_list[i]] = hw_component_list[i]

                hw_element_list.append(hw_element)
            self.hardware_part = hw_element_list

        self.prefix = part_list[0]

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
