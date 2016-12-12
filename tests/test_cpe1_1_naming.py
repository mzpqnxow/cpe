# -*- coding: utf-8 -*-

import unittest

from cpe.cpe1_1 import Cpe1_1


class Cpe1_1_Naming(unittest.TestCase):
    def test_input_cpe_is_always_stored(self):
        cpe_name = "cpe:/"
        cpe1_1 = Cpe1_1(cpe_name)
        self.assertEqual(cpe_name, cpe1_1.name)

    def test_create_cpe_name_without_parts(self):
        cpe_name = "cpe:/"
        cpe1_1 = Cpe1_1(cpe_name)
        result = {
            "prefix": "cpe:",
            "hardware": [],
        }

        self.assertEqual(cpe1_1.as_dict(), result)

    def test_create_cpe_name_with_only_one_hardware(self):
        cpe_name = "cpe:/cisco::3825"
        cpe1_1_hw = Cpe1_1(cpe_name)
        result = {
            "prefix": "cpe:",
            "hardware": [
                {
                    "vendor": "cisco",
                    "product": "",
                    "version": "3825",
                }
            ]
        }

        self.assertEqual(cpe1_1_hw.as_dict(), result)

    def test_get_hardware_part_of_cpe_name_without_parts(self):
        cpe_name = "cpe:/"
        cpe1_1 = Cpe1_1(cpe_name)
        self.assertListEqual(cpe1_1.get_hardware_part(), [])

    def test_get_os_part_of_cpe_name_without_parts(self):
        cpe_name = "cpe:/"
        cpe1_1 = Cpe1_1(cpe_name)
        self.assertListEqual(cpe1_1.get_os_part(), [])

    def test_get_application_part_of_cpe_name_without_parts(self):
        cpe_name = "cpe:/"
        cpe1_1 = Cpe1_1(cpe_name)
        self.assertListEqual(cpe1_1.get_application_part(), [])
