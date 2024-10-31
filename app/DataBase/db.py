import mysql.connector
import configparser


class DatabaseHandler:
    def __init__(self, config_file='db_config.ini'):
        self.config = configparser.ConfigParser()
        self.config.read(config_file)
        self.connection = None
        self.connect()

    def connect(self):
        """Establishes a connection to the database."""
        try:
            self.connection = mysql.connector.connect(
                host=self.config['mysql']['host'],
                database=self.config['mysql']['database'],
                user=self.config['mysql']['user'],
                password=self.config['mysql']['password'],
                port=self.config['mysql']['port']
            )
            print("Database connected successfully")
        except mysql.connector.Error as err:
            print(f"Error: {err}")

    def close(self):
        """Closes the database connection."""
        if self.connection and self.connection.is_connected():
            self.connection.close()
            print("Database connection closed")

    def add_record(self, from_, to, name, grade, phase, date, note="none"):
        """Inserts a new record into the points table."""
        try:
            cursor = self.connection.cursor()
            insert_query = """
                INSERT INTO points (`from`, `to`, `name`, `grade`, `phase`, `date`, `note`)
                VALUES ( %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(insert_query, (from_, to, name, grade, phase, date, note))
            self.connection.commit()
            print("Record added successfully")
        except mysql.connector.Error as err:
            print(f"Error: {err}")

    def get_all_records(self):
        """Fetches all records from the points table."""
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT * FROM points")
            results = cursor.fetchall()
            return results
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return []

    def get_tasks_name(self):
        """Fetches all records from the points table."""
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT * FROM tasks")
            results = cursor.fetchall()
            return results
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return []

    def get_all_phases_data(self):
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT * FROM phases")
            results = cursor.fetchall()
            return results
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return []