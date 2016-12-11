# -*- coding: utf-8 -*-

import unittest

from cpe.cpe1_1 import Cpe1_1


class Cpe1_1_Naming(unittest.TestCase):
    def test_create_cpe_name_without_parts(self):
        cpe_name = "cpe:/"
        cpe1_1 = Cpe1_1(cpe_name)
        self.assertEqual(cpe_name, cpe1_1.name)

    def test_get_hardware_part_of_cpe_name_without_parts(self):
        cpe_name = "cpe:/"
        cpe1_1 = Cpe1_1(cpe_name)
        self.assertListEqual(cpe1_1.get_hardware_part(), [])
