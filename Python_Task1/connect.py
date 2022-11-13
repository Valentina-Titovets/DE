import mysql.connector
from handling import DataBaseHandling
from set import CON_SETTINGS


class DataBaseConnector:
    """
    Class for operating with db
    """
    def __init__(self):
        self.connector = mysql.connector.connect(
            host=CON_SETTINGS['host'],
            user=CON_SETTINGS['user'],
            passwd=CON_SETTINGS['password'],
            database=CON_SETTINGS['database'],

        )
        self.cursor = self.connector.cursor()

    def create_db(self):
        self.cursor.execute(DataBaseHandling.create_db_query())

    def delete_db(self):
        self.cursor.execute(DataBaseHandling.delete_db_query())

    def drop_tables(self):
        for table in DataBaseHandling.drop_tables():
            self.cursor.execute(table)

    def create_tables(self):
        for table in DataBaseHandling.create_tables_query():
            self.cursor.execute(table)

    def rooms_inserting(self, rooms_list):
        for room in rooms_list:
            self.cursor.execute(DataBaseHandling.rooms_inserting(), (room['id'], room['name']))

    def students_inserting(self, students_list):
        for student in students_list:
            self.cursor.execute(DataBaseHandling.students_inserting(), (student['id'],
                                                                 student['name'],
                                                                 student['birthday'],
                                                                 student['room'],
                                                                 student['sex']))

    def commit(self):
        self.connector.commit()

    def selecting_data(self, query):
        self.cursor.execute(query)
        row_headers = [i[0] for i in self.cursor.description]
        results = self.cursor.fetchall()
        values_list = []
        for result in results:
            values_list.append(dict(zip(row_headers, result)))
        return values_list