import sqlite3 as sql

class database:
    def __init__(self, db_path):
        self._connection = sql.connect(db_path)
        self._connection.row_factory = sql.Row
        self._cursor = self._connection.cursor()
        self.params: dict = {}
        self.load_schema()

    def raw(self, request: str) -> list or bool:
        """
        RAW request. \n
        :param request: SQL request.
        :return:
        """
        try:
            self._cursor.execute(request)
            self._connection.commit()
            result = self._cursor.fetchall()

            return True if not result else result
        except sql.Error as e:
            print('[error] (raw) ' + str(e))
        return False

    def load_schema(self) -> None:
        """
        Load database schema. \n
        :return: None.
        """
        tables = self.get_tables()
        if not tables:
            return
        for table in tables:
            columns = self.get_columns(table)
            if not columns:
                continue
            self.params.update({table: columns})

    def get_tables(self) -> list or None:
        """
        GET TABLES in base. \n
        :return: list of tables or None.
        """
        tables: list = []
        request: str = "SELECT name FROM sqlite_schema WHERE type ='table' AND name NOT LIKE 'sqlite_%';"
        response = self.raw(request)
        if response is None or False:
            return None
        for table in response:
            tables.append(table['name'])
        return tables

    def get_columns(self, table: str) -> list or None:
        """
        GET COLUMNS of table. \n
        :param table: table name.
        :return: list of tables or None.
        """
        columns: list = []
        request: str = f"SELECT name FROM pragma_table_info('{table}');"
        response = self.raw(request)
        if response is None or False:
            return None
        for column in response:
            columns.append(column['name'])
        return columns
