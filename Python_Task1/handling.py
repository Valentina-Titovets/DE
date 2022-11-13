class DataBaseHandling:
    def create_db_query():
        return 'CREATE DATABASE result'

    def delete_db_query():
        return 'DROP DATABASE result'


    def create_tables_query():
        return ['''CREATE TABLE rooms (id INTEGER NOT NULL,
                                       name VARCHAR(30) NOT NULL,
                                       PRIMARY KEY(id))''',
                '''CREATE TABLE students (id INTEGER NOT NULL,
                                          name VARCHAR(30) NOT NULL,
                                          birthday DATETIME,
                                          room INTEGER NOT NULL,
                                          sex CHAR(1) NOT NULL,
                                          PRIMARY KEY(id),
                                          FOREIGN KEY(room) REFERENCES rooms(id) ON DELETE CASCADE)''',
                ]


    def drop_tables():
        return ['DROP TABLE students',
                'DROP TABLE rooms',
                ]

    @staticmethod
    def rooms_inserting():
        return 'INSERT INTO rooms(id, name) VALUES(%s, %s)'

    @staticmethod
    def students_inserting():
        return 'INSERT INTO students(id, name, birthday, room, sex) VALUES(%s, %s, %s, %s, %s)'

    @staticmethod
    def selecting_from_db():
        queries = {'rooms_and_students_quantity': '''SELECT rooms.id as room_id,
                                                            rooms.name as room_name,
                                                            COUNT(students.id) as quantity 
                                                     FROM Rooms JOIN students ON rooms.id = students.room
                                                     GROUP BY rooms.id''',

                   'top5_rooms_with_min_avg_age': '''SELECT rooms.id as room_id,
                                                            rooms.name as room_name,
                                                            CAST(AVG(TIMESTAMPDIFF(YEAR,students.birthday,NOW())) as float) as avg_age
                                                     FROM rooms JOIN students ON rooms.id = students.room
                                                     GROUP BY rooms.id
                                                     ORDER BY avg_age
                                                     LIMIT 5''',

                   'top5_rooms_with_max_age_diff': '''SELECT rooms.id as room_id,
                                                      rooms.name as room_name,
                                                      TIMESTAMPDIFF(YEAR,MIN(students.birthday),MAX(students.birthday))
                                                                    as age_diff
                                                      FROM rooms
                                                      JOIN students ON rooms.id = students.room
                                                      GROUP BY rooms.id
                                                      ORDER BY age_diff DESC
                                                      LIMIT 5''',

                   'rooms_with_M_and_F_sex': '''SELECT rooms.id as room_id,
                                                       rooms.name as room_name
                                                       FROM rooms JOIN students ON rooms.id = students.room
                                                       GROUP BY rooms.id
                                                       HAVING COUNT(DISTINCT students.sex) > 1''',
                    }
        return queries