from typing import List
import re
import logging
import os
import mysql.connector


PII_FIELDS = ("name", "email", "phone", "ssn", "password")


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str):
    return re.sub(f"({'|'.join(map(re.escape, fields))})=[^{separator}]*",
                  lambda m: f"{m.group(1)}={redaction}", message)


def get_logger() -> logging.Logger:
    """Creates and returns a logger with specified settings"""

    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(RedactingFormatter(PII_FIELDS))
    logger.addHandler(stream_handler)
    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """Connects MySQL database using credentials from environment variables"""

    db_user = os.getenv('PERSONAL_DATA_DB_USERNAME', 'root')
    db_pwd = os.getenv('PERSONAL_DATA_DB_PASSWORD', '')
    db_host = os.getenv('PERSONAL_DATA_DB_HOST', 'localhost')
    db_name = os.getenv('PERSONAL_DATA_DB_NAME')
    db_connection = mysql.connector.connect(
        user=db_user,
        password=db_pwd,
        host=db_host,
        database=db_name
    )

    return db_connection


def main():
    """Main function"""
    info_logger = get_logger()
    conn = get_db()
    fields = "name,email,phone,ssn,password,ip,last_login,user_agent"
    columns = fields.split(',')
    query = "SELECT {} FROM users;".format(fields)
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    for row in results:
        data = dict(zip(columns, row))
        print(data)
    cursor.close()
    conn.close()


class RedactingFormatter(logging.Formatter):
    """
    Redacting Formatter class
    """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]) -> str:
        """
        initialises the class
        """
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """
        formatting method 2 handle results
        """
        original_message = super().format(record)
        return filter_datum(self.fields, self.REDACTION,
                            original_message, self.SEPARATOR)
