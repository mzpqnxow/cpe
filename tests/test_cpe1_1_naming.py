# -*- coding: utf-8 -*-

import unittest

from cpe.cpe1_1 import Cpe1_1


class Cpe1_1_Naming(unittest.TestCase):
    def test_input_cpe_is_always_stored(self):
        cpe_name = "cpe:/"
        cpe1_1 = Cpe1_1(cpe_name)
        self.assertEqual(cpe_name, cpe1_1.name)

    def test_version_of_cpe_1_1_is_1_1(self):
        cpe_name = "cpe:/"
        cpe1_1 = Cpe1_1(cpe_name)
        self.assertEqual("1.1", cpe1_1.version)

    def test_create_cpe_name_without_parts(self):
        cpe_name = "cpe:/"
        cpe1_1 = Cpe1_1(cpe_name)

        self.assertEqual(cpe1_1.prefix, "cpe:")
        self.assertEqual(cpe1_1.hardware_part, [])
        self.assertEqual(cpe1_1.os_part, [])
        self.assertEqual(cpe1_1.application_part, [])

    def test_create_cpe_name_with_only_one_hardware(self):
        cpe_name = "cpe:/cisco::3825"
        cpe1_1_hw = Cpe1_1(cpe_name)
        hardware_part = [
            {
                "vendor": "cisco",
                "product": "",
                "version": "3825",
            }
        ]

        self.assertEqual(cpe1_1_hw.prefix, "cpe:")
        self.assertEqual(cpe1_1_hw.hardware_part, hardware_part)
        self.assertEqual(cpe1_1_hw.os_part, [])
        self.assertEqual(cpe1_1_hw.application_part, [])

    def test_create_cpe_name_with_more_than_one_hardware(self):
        cpe_name = "cpe:/juniper:m-series:m7i;juniper:es-pic"
        cpe1_1_hw = Cpe1_1(cpe_name)
        hardware_part = [
            {
                "vendor": "juniper",
                "product": "m-series",
                "version": "m7i",
            },
            {
                "vendor": "juniper",
                "product": "es-pic",
            }
        ]

        self.assertEqual(cpe1_1_hw.prefix, "cpe:")
        self.assertEqual(cpe1_1_hw.hardware_part, hardware_part)
        self.assertEqual(cpe1_1_hw.os_part, [])
        self.assertEqual(cpe1_1_hw.application_part, [])

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

    def test_create_cpe_name_with_only_one_vendor_element(self):
        cpe_name = "cpe:///vendor"
        cpe1_1_hw = Cpe1_1(cpe_name)
        application_part = [
            {
                "vendor": "vendor",
            }
        ]

        self.assertEqual(cpe1_1_hw.prefix, "cpe:")
        self.assertEqual(cpe1_1_hw.hardware_part, [])
        self.assertEqual(cpe1_1_hw.os_part, [])
        self.assertEqual(cpe1_1_hw.application_part, application_part)

    def test_create_cpe_name_with_only_one_product_element(self):
        cpe_name = "cpe:///:product"
        cpe1_1_hw = Cpe1_1(cpe_name)
        application_part = [
            {
                "vendor": "",
                "product": "product",
            }
        ]

        self.assertEqual(cpe1_1_hw.prefix, "cpe:")
        self.assertEqual(cpe1_1_hw.hardware_part, [])
        self.assertEqual(cpe1_1_hw.os_part, [])
        self.assertEqual(cpe1_1_hw.application_part, application_part)

    def test_create_cpe_name_with_only_one_version_element(self):
        cpe_name = "cpe:///::version"
        cpe1_1_hw = Cpe1_1(cpe_name)
        application_part = [
            {
                "vendor": "",
                "product": "",
                "version": "version",
            }
        ]

        self.assertEqual(cpe1_1_hw.prefix, "cpe:")
        self.assertEqual(cpe1_1_hw.hardware_part, [])
        self.assertEqual(cpe1_1_hw.os_part, [])
        self.assertEqual(cpe1_1_hw.application_part, application_part)

    def test_get_cpe_name_as_dictionary(self):
        cpe_name = ("cpe:"
                    "/h1_vendor:h1_product:h1_version;h2_product"
                    "/sw_vendor:sw_product"
                    "/app_vendor::app_version")
        cpe1_1_hw = Cpe1_1(cpe_name)
        result = {
            "prefix": "cpe:",
            "hardware": [
                {
                    "vendor": "h1_vendor",
                    "product": "h1_product",
                    "version": "h1_version",
                },
                {
                    "vendor": "h2_product",
                }
            ],
            "os": [
                {
                    "vendor": "sw_vendor",
                    "product": "sw_product",
                },
            ],
            "application": [
                {
                    "vendor": "app_vendor",
                    "product": "",
                    "version": "app_version",
                },
            ]
        }

        self.assertEqual(cpe1_1_hw.as_dict(), result)
