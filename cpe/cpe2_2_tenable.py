#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This file is part of cpe package.

This module is used to the treatment of identifiers
of IT platforms (hardware, operating systems or applications of system)
in accordance with version 2.2 of CPE (Common Platform Enumeration)
specification.

Copyright (C) 2013  Alejandro Galindo García, Roberto Abdelkader Martínez Pérez
Portions (C) 2022  Adam Greene

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
import re

from cpe.comp.cpecomp2_2 import CPEComponent2_2
from cpe.comp.cpecomp_logical import CPEComponentLogical
from .cpe import CPE
from .cpe2_3_wfn import CPE2_3_WFN
from .comp.cpecomp import CPEComponent
from .comp.cpecomp2_2_tenable import CPEComponent2_2_TENABLE
from .comp.cpecomp2_3_wfn import CPEComponent2_3_WFN
from .comp.cpecomp_empty import CPEComponentEmpty
from .comp.cpecomp_undefined import CPEComponentUndefined


_logger = logging.getLogger(__name__)


class CPE2_2_TENABLE(CPE):
    """
    Implementation of version 2.2 of CPE specification.

    A CPE Name is a percent-encoded URI with each name
    starting with the prefix (the URI scheme name) 'cpe:'.

    Each platform can be broken down into many distinct parts.
    A CPE Name specifies a simple part and is used to identify
    any platform that matches the description of that part.

    The distinct parts are:

    - Hardware part: the physical platform supporting the IT system.
    - Operating system part: the operating system controls and manages the
      IT hardware.
    - Application part: software systems, services, servers, and packages
      installed on the system.

    CPE Name syntax:

        cpe:/{part}:{vendor}:{product}:{version}:{update}:{edition}:{language}
    """

    ###############
    #  CONSTANTS  #
    ###############

    #: Version of CPE Name
    VERSION = CPE.VERSION_2_2_TENABLE
    COMPONENT_CLS = CPEComponent2_2_TENABLE

    ###############
    #  VARIABLES  #
    ###############

    # Compilation of regular expression associated with components
    # of CPE Name
    _part = "?P<{0}>(h|o|a)".format(COMPONENT_CLS.ATT_PART)
    _vendor = "?P<{0}>[^:]+".format(COMPONENT_CLS.ATT_VENDOR)
    _product = "?P<{0}>[^:]+".format(COMPONENT_CLS.ATT_PRODUCT)
    _package = "?P<{0}>[^:]+".format(COMPONENT_CLS.ATT_PACKAGE)

    _parts_pattern = "^p-cpe:/({0})?(:({1})?)?(:({2})?)?(:({3})?)?$".format(
        _part, _vendor, _product, _package)
    _parts_rxc = re.compile(_parts_pattern)

    ####################
    #  OBJECT METHODS  #
    ####################

    def __len__(self):
        """
        Returns the number of components of CPE Name.

        :returns: count of components of CPE Name
        :rtype: int
        """

        prefix = "p-cpe:/"
        data = self.cpe_str[len(prefix):]

        if data == "":
            return 0

        count = data.count(self.COMPONENT_CLS.SEPARATOR_COMP)

        return count + 1

    def __new__(cls, cpe_str, *args, **kwargs):
        """
        Create a new CPE Name of version 2.2.

        :param string cpe_str: CPE Name string
        :returns: CPE object of version 2.2 of CPE specification.
        :rtype: CPE2_2
        """

        return dict.__new__(cls)

    def get_package(self):
        """
        Returns the vendor name of CPE Name as a list.
        According to the CPE version,
        this list can contains one or more items.

        :returns: Value of vendor attribute as string list.
        :rtype: list
        """
        return self.get_attribute_values(self.COMPONENT_CLS.ATT_PACKAGE)

    def _parse(self):
        """
        Checks if CPE Name is valid.

        :returns: None
        :exception: ValueError - bad-formed CPE Name
        """

        # CPE Name must not have whitespaces
        if self._str.find(" ") != -1:
            msg = "Bad-formed CPE Name: it must not have whitespaces"
            raise ValueError(msg)

        # Partitioning of CPE Name
        parts_match = self._parts_rxc.match(self._str)
        # Validation of CPE Name parts
        if parts_match is None:
            msg = "Bad-formed CPE Name: validation of parts failed"
            raise ValueError(msg)

        components = dict()
        parts_match_dict = parts_match.groupdict()

        for ck in self.COMPONENT_CLS.CPE_COMP_KEYS:
            if ck in parts_match_dict:
                value = parts_match.group(ck)

                if value == CPEComponent2_2.VALUE_UNDEFINED:
                    comp = CPEComponentUndefined()
                elif value == CPEComponent2_2.VALUE_EMPTY:
                    comp = CPEComponentEmpty()
                else:
                    try:
                        _logger.debug(f'ck=%s, value=%s', ck, value)
                        comp = self.COMPONENT_CLS(value, ck)
                    except ValueError:
                        errmsg = "Bad-formed CPE Name: not correct value: {0}".format(value)
                        raise ValueError(errmsg)
            else:
                # Component not exist in this version of CPE
                comp = CPEComponentUndefined()

            components[ck] = comp

        # Adds the components of version 2.3 of CPE not defined in version 2.2
        for ck2 in self.COMPONENT_CLS.CPE_COMP_KEYS_EXTENDED:
            if ck2 not in components.keys():
                components[ck2] = CPEComponentUndefined()

        # #######################
        #  Storage of CPE Name  #
        # #######################

        # If part component is undefined, store it in the part without name
        if components[CPEComponent.ATT_PART] == CPEComponentUndefined():
            system = self.COMPONENT_CLS.VALUE_PART_UNDEFINED
        else:
            system = parts_match.group(self.COMPONENT_CLS.ATT_PART)

        self._create_cpe_parts(system, components)

        # Adds the undefined parts
        for sys in self.COMPONENT_CLS.SYSTEM_VALUES:
            if sys != system:
                pk = CPE._system_and_parts[sys]
                self[pk] = []

    def old_repr(self):
        return self.__str__

    def __repr__(self):
        """
        Returns a unambiguous representation of CPE Name.

        :returns: Representation of CPE Name as string
        :rtype: string
        """

        txt_parts = []

        for pk in self.CPE_PART_KEYS:
            txt_parts.append(pk)

            txt_elements = [self._PREFIX_ELEMENTS]

            elements = self.get(pk)

            for elem in elements:
                txt_elem = [self._PREFIX_ELEM]

                for i in range(0, len(self.COMPONENT_CLS.CPE_COMP_KEYS_EXTENDED)):
                    txt_comp = []
                    ck = self.COMPONENT_CLS.ordered_comp_parts.get(i)
                    _logger.debug(f'trying to get {ck} ...')
                    comp = elem.get(ck)

                    if isinstance(comp, CPEComponentLogical):
                        value = comp.__str__()
                    else:
                        value = comp.get_value()

                    txt_comp.append("     ")
                    txt_comp.append(ck)
                    txt_comp.append(" = ")
                    txt_comp.append(value)

                    txt_elem.append("".join(txt_comp))

                if len(txt_elem) == 1:
                    # There are no components
                    txt_elem = [" []"]
                else:
                    txt_elem.append(self._SUFFIX_ELEM)

                txt_elements.append("\n".join(txt_elem))

            if len(txt_elements) == 1:
                # There are no elements
                txt_elements = [" []"]
            else:
                txt_elements.append(self._SUFFIX_ELEMENTS)

            txt_parts.append("\n".join(txt_elements))

        return "\n".join(txt_parts)

    def as_wfn(self):
        """
        Returns the CPE Name as WFN string of version 2.3.
        Only shows the first seven components.

        :return: CPE Name as WFN string
        :rtype: string
        :exception: TypeError - incompatible version
        """

        wfn = [CPE2_3_WFN.CPE_PREFIX]

        for ck in self.COMPONENT_CLS.CPE_COMP_KEYS:
            lc = self._get_attribute_components(ck)

            comp = lc[0]

            if isinstance(comp, (CPEComponentEmpty, CPEComponentUndefined)):
                # Do not set the attribute
                continue

            v = [
                ck, "=",
                # Get the value of WFN of component
                '"', comp.as_wfn(), '"']

            # Append v to the WFN and add a separator
            wfn.append("".join(v))
            wfn.append(CPEComponent2_3_WFN.SEPARATOR_COMP)

        # Del the last separator
        wfn = wfn[:-1]

        # Return the WFN string
        wfn.append(CPE2_3_WFN.CPE_SUFFIX)

        return "".join(wfn)

    def get_attribute_values(self, att_name):
        """
        Returns the values of attribute "att_name" of CPE Name.
        By default a only element in each part.

        :param string att_name: Attribute name to get
        :returns: List of attribute values
        :rtype: list
        :exception: ValueError - invalid attribute name
        """

        lc = []

        if not self.COMPONENT_CLS.is_valid_attribute(att_name):
            errmsg = "Invalid attribute name: {0}".format(att_name)
            raise ValueError(errmsg)

        for pk in self.CPE_PART_KEYS:
            elements = self.get(pk)
            for elem in elements:
                comp = elem.get(att_name)

                if isinstance(comp, (CPEComponentEmpty, CPEComponentUndefined)):
                    value = self.COMPONENT_CLS.VALUE_EMPTY
                else:
                    value = comp.get_value()
                lc.append(value)
        return lc


if __name__ == "__main__":
    import doctest
    doctest.testmod()
    doctest.testfile("tests/testfile_cpe2_2_tenable.txt")
