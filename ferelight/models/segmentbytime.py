from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from ferelight.models.base_model import Model
from ferelight import util


class Segmentbytime(Model):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.
    """

    def __init__(self, objectid=None, timestamp=None):  # noqa: E501
        """Segmentbytime - a model defined in OpenAPI

        :param objectid: The objectid of this Segmentbytime.  # noqa: E501
        :type objectid: str
        :param timestamp: The timestamp of this Segmentbytime.  # noqa: E501
        :type timestamp: float
        """
        self.openapi_types = {
            'objectid': str,
            'timestamp': float
        }

        self.attribute_map = {
            'objectid': 'objectid',
            'timestamp': 'timestamp'
        }

        self._objectid = objectid
        self._timestamp = timestamp

    @classmethod
    def from_dict(cls, dikt) -> 'Segmentbytime':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The segmentbytime of this Segmentbytime.  # noqa: E501
        :rtype: Segmentbytime
        """
        return util.deserialize_model(dikt, cls)

    @property
    def objectid(self) -> str:
        """Gets the objectid of this Segmentbytime.

        The unique identifier of the object.  # noqa: E501

        :return: The objectid of this Segmentbytime.
        :rtype: str
        """
        return self._objectid

    @objectid.setter
    def objectid(self, objectid: str):
        """Sets the objectid of this Segmentbytime.

        The unique identifier of the object.  # noqa: E501

        :param objectid: The objectid of this Segmentbytime.
        :type objectid: str
        """
        if objectid is None:
            raise ValueError("Invalid value for `objectid`, must not be `None`")  # noqa: E501

        self._objectid = objectid

    @property
    def timestamp(self) -> float:
        """Gets the timestamp of this Segmentbytime.

        Timestamp to locate in seconds.  # noqa: E501

        :return: The timestamp of this Segmentbytime.
        :rtype: float
        """
        return self._timestamp

    @timestamp.setter
    def timestamp(self, timestamp: float):
        """Sets the timestamp of this Segmentbytime.

        Timestamp to locate in seconds.  # noqa: E501

        :param timestamp: The timestamp of this Segmentbytime.
        :type timestamp: float
        """
        if timestamp is None:
            raise ValueError("Invalid value for `timestamp`, must not be `None`")  # noqa: E501

        self._timestamp = timestamp
