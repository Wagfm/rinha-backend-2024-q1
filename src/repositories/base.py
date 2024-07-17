import logging
import os
from functools import wraps
from typing import Callable

import psycopg
from psycopg_pool import ConnectionPool

from database.row_factory import DictRowFactory


class BaseRepository:
    _cursor: psycopg.Cursor | None

    def __init__(self):
        host = os.environ["POSTGRES_HOST"]
        port = os.environ["POSTGRES_PORT"]
        dbname = os.environ["POSTGRES_DATABASE"]
        user = os.environ["POSTGRES_USER"]
        password = os.environ["POSTGRES_PASSWORD"]
        self._connection_info = f"""
            host={host}
            port={port}
            dbname={dbname}
            user={user}
            password={password}
        """
        self._cursor = None
        logging.getLogger("psycopg.pool").setLevel(logging.ERROR)
        logging.getLogger("psycopg.pool").disabled = True
        self._pool = ConnectionPool(self._connection_info, min_size=20, max_size=60, open=True)
        self._setup_table()

    @staticmethod
    def _with_connection(function: Callable) -> Callable:
        @wraps(function)
        def with_connection(self: "BaseRepository", *args, **kwargs):
            try:
                with self._pool.connection() as connection:
                    with connection.cursor(row_factory=DictRowFactory) as cursor:
                        self._cursor = cursor
                        result = function(self, *args, **kwargs)
                        self._cursor = None
            except psycopg.errors.IntegrityError:
                connection.rollback()
                raise
            except Exception:
                connection.rollback()
                raise
            else:
                connection.commit()
            return result

        return with_connection

    @_with_connection
    def _setup_table(self):
        with open("src/database/migration.sql", "r") as file:
            query = file.read().encode()
        self._cursor.execute(query)
