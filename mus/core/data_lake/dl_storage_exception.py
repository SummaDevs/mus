"""
Data lake storage exceptions
"""


class DlStorageException(Exception):
    """
    Data lake storage base exception
    """


class DlStorageLayerException(DlStorageException):
    # pylint: disable=C0115
    pass


class DlStorageNameObjException(DlStorageException):
    # pylint: disable=C0115
    pass


class DlStorageProviderException(DlStorageException):
    # pylint: disable=C0115
    pass


class DlStorageDataSetException(DlStorageException):
    # pylint: disable=C0115
    pass


class DlStorageFileFormatException(DlStorageException):
    # pylint: disable=C0115
    pass


class DlStorageTablePartitionException(DlStorageException):
    # pylint: disable=C0115
    pass


DL_EXCEPTION_DICT = {
    'layer': DlStorageLayerException,
    'provider': DlStorageProviderException,
    'name_obj': DlStorageNameObjException,
    'dataset_type': DlStorageDataSetException,
    'file_format': DlStorageFileFormatException,
    'table_partition': DlStorageTablePartitionException
}
