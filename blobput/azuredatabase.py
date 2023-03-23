import os
import logging
import pyodbc


import common


common.logger_config()
logger = logging.getLogger("file")


class AzureDB:
    def __init__(self):
        self.conn_str = 'DRIVER='+os.getenv('DB_DRIVER')+';SERVER=tcp:' + \
            os.getenv('DB_ADDR')+';PORT=1433;DATABASE=' + \
            os.getenv('DB_NAME')+';UID='+os.getenv('DB_USER') + \
            ';PWD='+os.getenv('DB_USER_PWD')
        self.cursor = None

    @common.log_function_call
    def connection(self, conn_str):
        """
        Establish connection to the database
        """
        # TODO error handling
        try:
            conn = pyodbc.connect(conn_str)
            self.cursor = conn.cursor()
            return self.cursor
        except pyodbc.Error as err:
            logging.critical('%s: %s', err.args[0], err.args[1])
            raise err

    @common.log_function_call
    def exec_stored_procedure(self, stored_procedure, *args):
        """
        Execute SQL stored procedures
        """
        try:
            query = f"exec {stored_procedure} "
            for count, value in enumerate(args):
                query += f'"{value}" '

            self.cursor.execute(query)
            return True
        except pyodbc.Error as err:
            logging.critical('%s: %s', err.args[0], err.args[1])
            raise err


if __name__ == '__main__':
    test = AzureDB()
    test.exec_stored_procedure("dbo.callcenter_insert_summary", "Customer first name", "Customer last name")
