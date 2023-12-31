"""
Avro writer
"""
import io

from fastavro import json_writer
from fastavro import parse_schema


class AvroJsonWriter:
    """
    Avro json writer, fast avro binding
    """

    def __init__(self, schema):
        """
        :param schema: avro schema
        :type schema: dict
        """
        self.parsed_schema = parse_schema(schema)
        self.file_obj = io.StringIO()

    def getvalue(self):
        """
        :return: file object value
        :rtype: binary
        """
        self.file_obj.seek(0)
        return self.file_obj.getvalue()

    def writerow(self, row):
        """
        Write single row

        :param row: row
        :type row: dict
        """

        json_writer(self.file_obj, self.parsed_schema, [row])

    def writerows(self, rows):
        """
        Write rows in bulk

        :param rows: multiple rows
        :type rows: list(dict)
        """
        json_writer(self.file_obj, self.parsed_schema, rows)

    def close(self):
        """
        Close file object
        """
        self.file_obj.close()
