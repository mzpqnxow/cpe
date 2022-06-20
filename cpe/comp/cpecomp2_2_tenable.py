#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This file is part of cpe package.

This module allows to store the value of the components of a CPE name
of version 2.2 of CPE (Common Platform Enumeration) specification.

Copyright (C) 2013  Alejandro Galindo García, Roberto Abdelkader Martínez Pérez

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Lesser General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License
along with this program. If not, see <http://www.gnu.org/licenses/>.

For any problems using the cpe package, or general questions and
feedback about it, please contact:

- Alejandro Galindo García: galindo.garcia.alejandro@gmail.com
- Roberto Abdelkader Martínez Pérez: robertomartinezp@gmail.com
"""
import logging

from .cpecomp_simple import CPEComponentSimple

import re

from .cpecomp import CPEComponent


_logger = logging.getLogger(__name__)


class CPEComponent2_2_TENABLE(CPEComponentSimple):
    """
    Represents a component of version 2.2 of CPE specification.

    TEST: simple value

    >>> value = "microsoft"
    >>> comp = CPEComponent2_2_TENABLE(value, CPEComponentSimple.ATT_VENDOR)
    """

    ###############
    #  CONSTANTS  #
    ###############

    #: Pattern used to check the value of component
    _VALUE_PATTERN = "^([\d\w\._\-~%]+)$"

    #: Separator of components of CPE name with URI style
    SEPARATOR_COMP = ":"

    #: Characters of version 2.2 of CPE name to convert
    #: to standard value (WFN value)
    NON_STANDARD_VALUES = [".", "-", "~", "%"]

    # Logical values in string format

    #: Logical value associated with a undefined component of CPE Name
    VALUE_UNDEFINED = None

    #: Logical value associated with a component without value set
    VALUE_EMPTY = ""

    #: Version 2.2_TENABLE of CPE component
    COMP_2_2_Tenable = "2.2_Tenable"

    COMP_TENABLE = "Tenable"

    #: List of attribute names associated with CPE Name components
    #: (versions 1.1 and 2.2 of CPE specification)
    CPE_COMP_KEYS = (CPEComponent.ATT_PART,
                     CPEComponent.ATT_VENDOR,
                     CPEComponent.ATT_PRODUCT,
                     CPEComponent.ATT_PACKAGE)

    #: List of attribute names associated with CPE Name components
    #: of version 2.3
    CPE_COMP_KEYS_EXTENDED = (CPEComponent.ATT_PART,
                              CPEComponent.ATT_VENDOR,
                              CPEComponent.ATT_PRODUCT,
                              CPEComponent.ATT_PACKAGE,
                              CPEComponent.ATT_OTHER)

    ###############
    #  VARIABLES  #
    ###############
    #: Order of attributes of CPE Name components
    ordered_comp_parts = {0: CPEComponent.ATT_PART,
                          1: CPEComponent.ATT_VENDOR,
                          2: CPEComponent.ATT_PRODUCT,
                          3: CPEComponent.ATT_PACKAGE,
                          4: CPEComponent.ATT_OTHER}
    #: Compilation of pattern used to check the value of component
    _value_rxc = re.compile(_VALUE_PATTERN)

    ####################
    #  OBJECT METHODS  #
    ####################

    def _parse(self, comp_att):
        """
        Check if the value of component is correct in the attribute "comp_att".

        :param string comp_att: attribute associated with value of component
        :returns: None
        :exception: ValueError - incorrect value of component
        """

        errmsg = "Invalid attribute '{0}'".format(comp_att)

        if not self.is_valid_attribute(comp_att):
            raise ValueError(errmsg)

        comp_str = self._encoded_value

        errmsg = "Invalid value of attribute '{0}': {1}".format(
            comp_att, comp_str)

        comp_map_validator = {
            CPEComponentSimple.ATT_PART: self._is_valid_part,
            CPEComponentSimple.ATT_LANGUAGE: self._is_valid_language,
            CPEComponentSimple.ATT_EDITION: self._is_valid_edition,
            CPEComponentSimple.ATT_PACKAGE: self._is_valid_package,
        }

        validator = comp_map_validator.get(comp_att, self._is_valid_value)
        _logger.debug('Using validator function=%s for comp_att=%s', validator.__name__, comp_att)
        if not validator():
            raise ValueError(errmsg)

    def __repr__(self):
        """
        Returns a unambiguous representation of CPE component.

        :returns: Representation of CPE component as string
        :rtype: string
        """

        return "{0}({1})".format(self.__class__.__name__, self.get_value())

    def _decode(self):
        """
        Convert the encoded value of component to standard value (WFN value).
        """

        result = []
        idx = 0
        s = self._encoded_value

        while idx < len(s):
            # Get the idx'th character of s
            c = s[idx]

            if c in self.NON_STANDARD_VALUES:
                # Escape character
                result.append("\\")
                result.append(c)
            else:
                # Do nothing
                result.append(c)

            idx += 1

        self._standard_value = "".join(result)

    @classmethod
    def is_valid_attribute(cls, att_name):
        """
        Check if input attribute name is correct.

        :param string att_name: attribute name to check
        :returns: True is attribute name is valid, otherwise False
        :rtype: boolean

        TEST: a wrong attribute

        >>> from .cpecomp import CPEComponent2_2_TENABLE
        >>> att = CPEComponent2_2_TENABLE.ATT_PRODUCT
        >>> CPEComponent.is_valid_attribute(att)
        True
        """
        if att_name not in CPEComponent2_2_TENABLE.CPE_COMP_KEYS_EXTENDED:
            _logger.debug('err, %s not in (%s)', att_name, '|'.join(cls.CPE_COMP_KEYS_EXTENDED))
        return att_name in CPEComponent2_2_TENABLE.CPE_COMP_KEYS_EXTENDED

    def _is_valid_package(self):
        """
        Return True if the value of component in attribute "part" is valid,
        and otherwise False.

        :returns: True if value of component is valid, False otherwise
        :rtype: boolean
        """
        return self._is_valid_value() is not None

    def _is_valid_value(self):
        """
        Return True if the value of component in generic attribute is valid,
        and otherwise False.

        :returns: True if value is valid, False otherwise
        :rtype: boolean
        """
        comp_str = self._encoded_value
        _logger.debug(f'checking validity of value: %s', comp_str)
        match = self._value_rxc.match(comp_str) is not None
        if not match:
            _logger.debug('err, no match on %s', comp_str)
        return match

    def set_value(self, comp_str, comp_att):
        """
        Set the value of component. By default, the component has a simple
        value.

        :param string comp_str: new value of component
        :param string comp_att: attribute associated with value of component
        :returns: None
        :exception: ValueError - incorrect value of component
        """

        old_value = self._encoded_value
        self._encoded_value = comp_str

        # Check the value of component
        try:
            self._parse(comp_att)
        except ValueError:
            # Restore old value of component
            self._encoded_value = old_value
            raise

        # Convert encoding value to standard value (WFN)
        self._decode()


if __name__ == "__main__":
    import doctest
    doctest.testmod()
    doctest.testfile("../tests/testfile_cpecomp2_2_tenable.txt")
