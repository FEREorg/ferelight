from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from ferelight.models.base_model import Model
from ferelight import util


class SegmentbytimePostRequest(Model):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.
    """

    def __init__(self, database=None, objectid=None, timestamp=None):  # noqa: E501
        """SegmentbytimePostRequest - a model defined in OpenAPI

        :param database: The database of this SegmentbytimePostRequest.  # noqa: E501
        :type database: str
        :param objectid: The objectid of this SegmentbytimePostRequest.  # noqa: E501
        :type objectid: str
        :param timestamp: The timestamp of this SegmentbytimePostRequest.  # noqa: E501
        :type timestamp: float
        """
        self.openapi_types = {
            'database': str,
            'objectid': str,
            'timestamp': float
        }

        self.attribute_map = {
            'database': 'database',
            'objectid': 'objectid',
            'timestamp': 'timestamp'
        }

        self._database = database
        self._objectid = objectid
        self._timestamp = timestamp

    @classmethod
    def from_dict(cls, dikt) -> 'SegmentbytimePostRequest':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The _segmentbytime_post_request of this SegmentbytimePostRequest.  # noqa: E501
        :rtype: SegmentbytimePostRequest
        """
        return util.deserialize_model(dikt, cls)

    @property
    def database(self) -> str:
        """Gets the database of this SegmentbytimePostRequest.

        The name of the database to query.  # noqa: E501

        :return: The database of this SegmentbytimePostRequest.
        :rtype: str
        """
        return self._database

    @database.setter
    def database(self, database: str):
        """Sets the database of this SegmentbytimePostRequest.

        The name of the database to query.  # noqa: E501

        :param database: The database of this SegmentbytimePostRequest.
        :type database: str
        """

        self._database = database

    @property
    def objectid(self) -> str:
        """Gets the objectid of this SegmentbytimePostRequest.

        The object ID to find the segment in.  # noqa: E501

        :return: The objectid of this SegmentbytimePostRequest.
        :rtype: str
        """
        return self._objectid

    @objectid.setter
    def objectid(self, objectid: str):
        """Sets the objectid of this SegmentbytimePostRequest.

        The object ID to find the segment in.  # noqa: E501

        :param objectid: The objectid of this SegmentbytimePostRequest.
        :type objectid: str
        """

        self._objectid = objectid

    @property
    def timestamp(self) -> float:
        """Gets the timestamp of this SegmentbytimePostRequest.

        The timestamp to match against.  # noqa: E501

        :return: The timestamp of this SegmentbytimePostRequest.
        :rtype: float
        """
        return self._timestamp

    @timestamp.setter
    def timestamp(self, timestamp: float):
        """Sets the timestamp of this SegmentbytimePostRequest.

        The timestamp to match against.  # noqa: E501

        :param timestamp: The timestamp of this SegmentbytimePostRequest.
        :type timestamp: float
        """

        self._timestamp = timestamp
