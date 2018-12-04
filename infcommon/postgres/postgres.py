# -*- coding: utf-8 -*-

import psycopg2 as pg
from retrying import retry


class PostgresClient(object):

    def __init__(self, db_uri):
        self._db_uri = db_uri
        self._connection = None

    def execute(self, query, args=None):
        result = []
        with self._cursor() as my_cursor:
            my_cursor.execute(query, args)
            try:
                result = my_cursor.fetchall()
            except pg.ProgrammingError:
                pass
        return result

    def _cursor(self, retries=True):
        if retries:
            self._connection = self._unreliable_connection()
        else:
            self._connection = pg.connect(self._db_uri)

        self._connection.autocommit = True
        return self._connection.cursor()

    @retry(wait_exponential_multiplier=1000, wait_exponential_max=10000, stop_max_attempt_number=5)
    def _unreliable_connection(self):
        return pg.connect(self._db_uri)
