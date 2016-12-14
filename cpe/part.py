# -*- coding: utf-8 -*-


class CpePart(object):
    def __init__(self, part_data, part_type):
        self.part_data = part_data
        self.part_type = part_type
        self.element_list = []

        if len(part_data) > 0:
            self._parse_part()

    def _parse_part(self):
        component_key_list = ["vendor", "product", "version"]

        for elem in self.part_data.split(";"):
            component_list = elem.split(":")
            element = {}

            for i in range(0, len(component_list)):
                element[component_key_list[i]] = component_list[i]

            self.element_list.append(element)

    def as_dict(self):
        return self.element_list
