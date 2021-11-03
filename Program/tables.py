import sqlite3

database = 'main.db'
try:
    conn = sqlite3.connect(database, check_same_thread=False)
except Exception as e:
    print(f"Error connecting to database: {e}")

def execute(sql_cmd, values):
    """
    Takes an SQL command, and any values, then executes it
    using a cursor with the database connection.
    :param sql_cmd:
    :param values:
    :return:
    """
    cur = conn.cursor()
    cur.execute(sql_cmd, values)
    conn.commit()
    cur.close()

def get_all_rows(table):
    """
    Takes in a table name, and fetches every row in it.
    Returns a list of tuples with the rows information.
    :param table:
    :return: row_list
    """
    sql_command = f'''SELECT * FROM {table}'''

    cur = conn.cursor()
    cur.execute(sql_command)
    return cur.fetchall()

def get_programmes_list():
    """
    Gets all of the rows from the PROGRAMME table, and turns them
    into Programme objects, returns a list
    :return: list
    """
    return [Programme(tuple) for tuple in get_all_rows('PROGRAMME')]

class Programme:
    """
    Programme class, has its attributes, and an add method.
    """
    def __init__(self, tuple=(None, None, None)):
        self.id = tuple[0]
        self.name = tuple[1]
        self.level = tuple[2]

    def add(self):
        sql_cmd = f'''INSERT INTO PROGRAMME(programmeName, level) VALUES(?, ?)'''
        values = (self.name, self.level)
        execute(sql_cmd, values)

class Course:
    """
    Course class, has its attributes and add method.
    """
    def __init__(self, tuple=(None, None, None, None, None, None)):
        self.id = tuple[0]
        self.name = tuple[1]
        self.credits = tuple[2]
        self.fee = tuple[3]
        self.status = tuple[4]
        self.programmeID = tuple[5]

    def add(self):
        sql_cmd = f'''INSERT INTO COURSE(courseName, credits, fee, status, programmeID) VALUES(?, ?, ?, ?, ?)'''
        values = (self.name, self.credits, self.fee, self.status, self.programmeID)
        execute(sql_cmd, values)
