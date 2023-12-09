"""
An exhaustive enumerations all possible partition values
Please see. DL_PARTITION_DICT for details
"""
from enum import Enum
from enum import auto
from enum import unique


class AutoName(Enum):
    """
    Enum class to use name as enum code
    """

    def _generate_next_value_(self, start, count, last_values):
        """
        Enum interface
        """
        # pylint: disable=W0613,E0213
        return self


@unique
class DlLayer(AutoName):
    # pylint: disable=C0115
    raw = auto()
    std = auto()
    app = auto()
    sandbox = auto()


DL_LAYER_SET = {item.name for item in DlLayer}


@unique
class DlProvider(AutoName):
    # pylint: disable=C0115
    brave1 = auto()


DL_PROVIDER_SET = {item.name for item in DlProvider}


@unique
class DlDatasetType(AutoName):
    # pylint: disable=C0115
    full = auto()
    delta = auto()
    agg = auto()
    meta = auto()


DL_DATASET_TYPE_SET = {item.name for item in DlDatasetType}


@unique
class DlFileFormat(AutoName):
    # pylint: disable=C0115
    json = auto()
    ndjson = auto()
    csv = auto()
    parquet = auto()
    orc = auto()
    avro = auto()
    arrow = auto()


DR_FILE_FORMAT_SET = {item.name for item in DlFileFormat}

DL_PARTITION_DICT = {
    'layer': DL_LAYER_SET,
    'provider': DL_PROVIDER_SET,
    'dataset_type': DL_DATASET_TYPE_SET,
    'file_format': DR_FILE_FORMAT_SET
}
