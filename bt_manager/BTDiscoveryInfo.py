from __future__ import unicode_literals
from xml.etree.ElementTree import XML
from bt_manager import SERVICES, ATTRIBUTES
import pprint


class BTDiscoveryInfo:
    """Parser for XML BT discovery service record provided by Bluez"""
    def __init__(self, text):
        tree = XML(text)
        rec = tree.iter().next()
        if (rec is not None):
            self._uuid = None
            self.__dict__ = self._parse_element(rec)

    def _parse_element(self, elem):
        if (elem.tag == 'record'):
            return {self._parse_element(k):
                    self._parse_element(list(k)[0])
                    for k in elem.findall('attribute')}
        elif (elem.tag == 'sequence'):
            return [self._parse_element(k) for k in list(elem)]
        elif (elem.tag == 'attribute'):
            attrib_id = elem.attrib['id'][2:].upper()  # Remove leading '0x'
            if (attrib_id in ATTRIBUTES['*']):
                return ATTRIBUTES['*'][attrib_id]
            elif (ATTRIBUTES.get(self._uuid)):
                return ATTRIBUTES[self._uuid].get(attrib_id, attrib_id)
            else:
                return attrib_id
        elif (elem.tag == 'uuid'):
            self._uuid = \
                elem.attrib['value'][2:].upper()  # Remove leading '0x'
            return {'uuid': SERVICES.get(self._uuid, self._uuid)}
        elif ('value' in elem.attrib):
            return elem.attrib['value']

    def __repr__(self):
        return pprint.pformat(self.__dict__)
