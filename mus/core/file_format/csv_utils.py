"""
In memory csv writer.
Important: only writerow_ts method is thread safe
"""

import csv
import io
from threading import Lock


# pylint: disable=R0903
class Gdelt20CsvDialect(csv.Dialect):
    """
    Pipeline standard csv dialect
    """
    delimiter = "\t"
    doublequote = True
    escapechar = "\\"
    lineterminator = '\n'
    quotechar = '"'
    quoting = csv.QUOTE_MINIMAL


# pylint: disable=R0903
class CsvMemDictReader:
    """
    Csv memory writer implementation
    """

    def __init__(self, data, dialect=Gdelt20CsvDialect):
        """
        :param data: csv data binary string
        :param dialect: csv dialect
        """
        self.csv_fo = io.StringIO(
            data.decode() if isinstance(data, bytes) else data)

        self.csv_reader = csv.DictReader(self.csv_fo, dialect=dialect)

    def __call__(self, *args, **kwargs):
        """
        :param args: _
        :param kwargs: _

        :return: iterator
        """
        try:
            for row in self.csv_reader:
                yield row
        finally:
            if self.csv_fo:
                self.csv_fo.close()


class CsvMemDictWriter:
    """
    In memory csv writer class
    """

    def __init__(self, fieldnames, dialect=Gdelt20CsvDialect):
        """
        :param fieldnames: csv fieldnames list
        :param dialect: csv dialect class
        """
        self.file_obj = io.StringIO()
        self.csv_writer = csv.DictWriter(
            self.file_obj,
            fieldnames=fieldnames,
            dialect=dialect
        )
        self.csv_writer.writeheader()

        self.lock = Lock()

    def getvalue(self):
        """
        Returns file object buffer value

        :return: str
        """
        self.file_obj.seek(0)
        return self.file_obj.getvalue()

    def writerow(self, row):
        """
        Write data row

        :param row: data dict
        """
        self.csv_writer.writerow(row)

    def writerow_ts(self, row):
        """
        Write data row thread safe

        :param row: data dict
        """
        self.lock.acquire()
        self.csv_writer.writerow(row)
        self.lock.release()

    def writerows(self, rows):
        """
        Write data rows

        :param rows: data dict
        """
        self.csv_writer.writerows(rows)

    def close(self):
        """
        Close file object
        """
        self.file_obj.close()
