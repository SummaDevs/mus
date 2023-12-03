"""
All python methods that read/write from the data lake buckets should use
these class methods to enforce data lake layout convention.
"""

import copy
import datetime
import re

from .dl_partition_enum import DL_PARTITION_DICT
from .dl_storage_exception import DL_EXCEPTION_DICT

KEY_PATTERN = '{layer}/{provider}/{table_obj}/{set_type}/{file_format}/' \
              '{table_partition}/{file_prefix}{file_name}{file_suffix}'


class DlS3Key:
    """
    This is a class that generates keys for data lake objects.
    """

    # pylint: disable=R0902
    def __init__(
            self,
            layer,
            provider,
            table_obj,
            dataset_type,
            file_format,
            table_partition=None):
        """
        :param layer: raw|std|app|sandbox
        :param provider: data provider, see provider enumeration
        :param table_obj: table object name
        :param dataset_type: data set semantic type full|delta|agg|meta
        :param file_format: file format, see files format enumeration
        :param table_partition: table data partition (date or field enum)
        """
        # pylint: disable=R0913
        self.name_obj_pattern = r'^[a-z][a-z0-9\-]+$'
        self.name_obj_re = re.compile(self.name_obj_pattern)

        self.name_suffix_obj_pattern = r'^[a-z0-9\-]+$'
        self.name_suffix_obj_re = re.compile(self.name_suffix_obj_pattern)

        self.table_partition_pattern = r'^([a-z0-9]+((?<!\/)\/(?!\/))?[a-z0-9]*)+$'
        self.table_partition_re = re.compile(self.table_partition_pattern)

        self.layer = self.validate_set_param(layer, 'layer')
        self.provider = self.validate_set_param(provider, 'provider')

        self.table_obj = self.validate_name_obj(table_obj)

        self.dataset_type = self.validate_set_param(
            dataset_type, 'dataset_type')
        self.file_format = self.validate_set_param(file_format, 'file_format')

        self.table_partition = self.validate_table_partition(table_partition)

        self.file_suffix_cnt = 0

    def get_key_path(self):
        """
        :return: key path without trailing slash
        """
        return '/'.join((
            self.layer,
            self.provider,
            self.table_obj,
            self.dataset_type,
            self.file_format,
            self.table_partition
        ))

    def get_key_file(self, file_name, file_prefix='', file_suffix=None):
        """
        :param file_name: file name part
        :param file_prefix: file prefix, default empty
        :param file_suffix: file prefix, if none will be generated sequence
        :return: normalized file name
        """
        file_name = self.validate_name_obj(file_name, 'file name')

        if file_prefix != '':
            file_prefix = self.validate_name_obj(
                file_prefix, 'file name prefix')

        if file_suffix is None:
            file_suffix = f'-{self.file_suffix_cnt:06}'
            self.file_suffix_cnt += 1
        elif file_suffix != '':
            file_suffix = self.validate_name_suffix_obj(
                file_suffix, 'file name suffix')

        return ''.join((
            file_prefix, file_name, file_suffix, '.', self.file_format
        ))

    def get_key(self, file_name, file_prefix='', file_suffix=None):
        """
        :param file_name: file name part
        :param file_prefix: file prefix, default empty
        :param file_suffix: file prefix, if none will be generated sequence
        :return: normalized S# key
        """
        return '/'.join((
            self.get_key_path(),
            self.get_key_file(file_name, file_prefix, file_suffix)
        ))

    def get_copy(
            self,
            layer=None,
            provider=None,
            table_obj=None,
            dataset_type=None,
            file_format=None,
            table_partition=None):
        """
        :param layer: raw|std|app|sandbox
        :param provider: data provider, see provider enumeration
        :param table_obj: table object name
        :param dataset_type: data set semantic type full|delta|agg|meta
        :param file_format: file format, see files format enumeration
        :param table_partition: table data partition (date or field enum)
        :return: copy of key gen class with are defined state
        """
        # pylint: disable=R0913
        copy_self = copy.deepcopy(self)
        copy_self.file_suffix_cnt = 0

        if layer is not None:
            copy_self.layer = self.validate_set_param(layer, 'layer')

        if provider is not None:
            copy_self.provider = self.validate_set_param(provider, 'provider')

        if table_obj is not None:
            copy_self.table_obj = self.validate_name_obj(table_obj)

        if dataset_type is not None:
            self.dataset_type = self.validate_set_param(
                dataset_type, 'dataset_type')

        if file_format is not None:
            self.file_format = self.validate_set_param(
                file_format, 'file_format')

        if table_partition is not None:
            self.table_partition = self.validate_table_partition(
                table_partition)

    @staticmethod
    def validate_set_param(val, val_name):
        """
        :param val: enumeration string to check
        :param val_name: value key name for enumeration check
        :return: normalized enumeration name
        """
        # pylint: disable=R0201
        val = str(val).lower()
        if val not in DL_PARTITION_DICT[val_name]:
            raise DL_EXCEPTION_DICT[val_name](
                f'Wrong {val_name} "{val}", permitted values are '
                f'{",".join(DL_PARTITION_DICT[val_name])}'
            )
        return val

    def validate_name_obj(self, val, val_name='table'):
        """
        :param val: name string
        :param val_name: name type for logging
        :return: normalized object name
        """
        val = str(val).lower()
        if not self.name_obj_re.match(val):
            raise DL_EXCEPTION_DICT['name_obj'](
                f'Wrong {val_name} obj "{val}", name should start with '
                f'a letter and include only lower case alphanumeric symbols '
                f'[{self.name_obj_pattern}]'
            )
        return val

    def validate_name_suffix_obj(self, val, val_name='table_suffix'):
        """
        :param val: name string
        :param val_name: name type for logging
        :return: normalized suffix
        """
        val = str(val).lower()
        if not self.name_suffix_obj_re.match(val):
            raise DL_EXCEPTION_DICT['name_obj'](
                f'Wrong {val_name} obj "{val}", suffix should'
                f'include only lower case alphanumeric symbols or -'
                f'[{self.name_suffix_obj_pattern}]'
            )
        return val

    def validate_table_partition(self, val):
        """
        :param val: table name string
        :return: normalized table name, raise exception
        """
        val = str(val or datetime.datetime.now().strftime('%Y/%m/%d'))
        if not self.table_partition_re.match(val):
            raise DL_EXCEPTION_DICT['table_partition'](
                f'Wrong table_partition "{val}", table partition should '
                f'include lower case alphanumeric and / symbols only '
                f'[{self.table_partition_pattern}]'
            )
        return val
