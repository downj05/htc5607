import sqlite3
from datetime import datetime

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


def get_enrolments_list():
    """
    Returns a list of Enrolment objects from the
    ENROLMENT table.
    :return: list
    """
    return [Enrolment(tuple) for tuple in get_all_rows('ENROLMENT')]


def get_assessments_list():
    """
    Returns a list of Assessment objects from the
    ASSESSMENT table.
    :return: list
    """
    return [Assessment(tuple) for tuple in get_all_rows('ASSESSMENT')]


def get_programmes_list(noassignments=False):
    """
    Gets all of the rows from the PROGRAMME table, and turns them
    into Programme objects, returns a list. Can specify wether the
    rows fetched
    :return: list
    """
    if noassignments is False:
        return [Programme(tuple) for tuple in get_all_rows('PROGRAMME')]
    else:
        '''
        Only returns programmes whos programmeID does NOT appear
        in the courses table.
        '''
        sql_cmd = '''SELECT * FROM PROGRAMME AS P
        WHERE P."programmeID" NOT IN (SELECT "programmeID" FROM COURSE)'''
        cur = conn.cursor()
        cur.execute(sql_cmd)
        return [Programme(tuple) for tuple in cur.fetchall()]


def get_courses_list(noassigments=False):
    """
    Gets all of the rows from the COURSE table, turns them into
    Course objects, returns a list. The user can specify wether
    these courses have any assignments aswell.
    :return: list
    """
    if noassigments is False:
        return [Course(tuple) for tuple in get_all_rows('COURSE')]
    else:
        '''
        Only returns courses who's courseID does NOT appear in
        the ASSIGNMENT table AND the ASSESSMENT table.
        '''
        sql_command = '''SELECT * FROM COURSE AS C
         WHERE C."courseID" NOT IN (SELECT "courseID" FROM ASSIGNMENT)
          AND C."courseID" NOT IN (SELECT "courseID" FROM ASSESSMENT)
		  AND C."courseID" NOT IN (SELECT "courseID" FROM ENROLMENT)'''

        cur = conn.cursor()
        cur.execute(sql_command)
        return [Course(tuple) for tuple in cur.fetchall()]


def get_course_from_id(id):
    """
    Gets a course object from an ID.
    :param id:
    :return: course
    """
    sql_command = f'''SELECT * FROM COURSE WHERE courseID=?'''

    cur = conn.cursor()
    cur.execute(sql_command, (id,))
    return Course(cur.fetchone())


def get_programme_from_id(id):
    """
    Gets a programme object from an ID.
    :param id:
    :return: programme
    """
    sql_command = f'''SELECT * FROM PROGRAMME WHERE ProgrammeID=?'''

    cur = conn.cursor()
    cur.execute(sql_command, (id,))
    return Programme(cur.fetchone())


def get_assessment_from_id(id):
    """
    Gets an assessment object from an ID
    :param id:
    :return: assessment
    """
    sql_command = f'''SELECT * FROM ASSESSMENT WHERE assessmentID=?'''

    cur = conn.cursor()
    cur.execute(sql_command, (id,))
    return Assessment(cur.fetchone())


def get_enrolments_from_course(course):
    course_id = course.id
    sql_cmd = f'''SELECT * FROM ENROLMENT AS E WHERE E."courseID" IN (SELECT "courseID" FROM COURSE WHERE "courseID" == ?)'''
    cur = conn.cursor()
    cur.execute(sql_cmd, (course_id,))
    return cur.fetchall()


def get_assessments_from_course(course):
    course_id = course.id
    sql_cmd = f'''SELECT * FROM ASSESSMENT AS E WHERE E."courseID" IN (SELECT "courseID" FROM COURSE WHERE "courseID" == ?)'''
    cur = conn.cursor()
    cur.execute(sql_cmd, (course_id,))
    return cur.fetchall()

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

    def update(self):
        sql_cmd = f'''UPDATE PROGRAMME SET programmeName = ?, level = ? WHERE programmeID = ?'''
        values = (self.name, self.level, self.id)
        execute(sql_cmd, values)

    def delete(self):
        sql_cmd = f'''DELETE FROM PROGRAMME WHERE programmeID = ?'''
        values = (self.id,)
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

    def update(self):
        sql_cmd = f'''UPDATE COURSE SET courseName = ?, credits = ?, fee = ?, status = ? WHERE courseID = ?'''
        values = (self.name, self.credits, self.fee, self.status, self.id)
        execute(sql_cmd, values)

    def delete(self):
        sql_cmd = f'''DELETE FROM COURSE WHERE courseID = ?'''
        values = (self.id,)
        execute(sql_cmd, values)


class Assessment:
    """
    Assessment class, has its attributes and a property
    for getting a courses name from its ID.
    """
    def __init__(self, tuple=(None, None, None, None, None, None, None)):
        self.id = tuple[0]
        self.number = tuple[1]
        self.name = tuple[2]
        self.type = tuple[3]
        self.weighting = tuple[4]
        self.maximumMark = tuple[5]
        self.courseID = tuple[6]

    @property
    def course_name(self):
        # Gets a course name from the objects course id
        sql_command = f'''SELECT courseName FROM COURSE WHERE courseID=?'''

        cur = conn.cursor()
        cur.execute(sql_command, (self.courseID,))
        return cur.fetchone()[0]


class Enrolment:
    """
    Enrolment class, has its attributes and takes in
    a tuple upon creation. Has a year string property
    to convert the timestamp into its year, also has
    a student name property to get their name from the
    objects student ID.
    """
    def __init__(self, tuple):
        self.id = tuple[0]
        self.year = tuple[1]
        self.semester = tuple[2]
        self.status = tuple[3]
        self.studentID = tuple[4]
        self.courseID = tuple[5]

    @property
    def year_string(self):
        return datetime.utcfromtimestamp(self.year).strftime('%Y')

    @property
    def student_name(self):
        # Gets a course name from the objects course id
        sql_command = f'''SELECT firstName, lastName FROM STUDENT WHERE studentID=?'''

        cur = conn.cursor()
        cur.execute(sql_command, (self.studentID,))
        firstName, lastName = cur.fetchone()
        return firstName+" "+lastName


class Result:
    """
    Result class, ties to the RESULT table, can be added
    with the add method and is created with a tuple.
    """
    def __init__(self, tuple):
        self.assessmentID = tuple[0]
        self.enrolmentID = tuple[1]
        self.resultDate = tuple[2]
        self.mark = tuple[3]

    def add(self):
        # Add the result object to the RESULT table
        sql_cmd = f'''INSERT INTO RESULT(assessmentID, enrolmentID, resultDate, mark) VALUES(?, ?, ?, ?)'''
        values = (self.assessmentID, self.enrolmentID, self.resultDate, self.mark)
        execute(sql_cmd, values)

    def check_assignments(self):
        '''
        Check if the results assessmentID and enrolmentID are already
        part of a result.
        Returns True if the result is already assigned, False if otherwise.
        :return: boolean
        '''
        sql_cmd = f'''SELECT * FROM RESULT WHERE assessmentID=? AND enrolmentID=?'''
        values = (self.assessmentID, self.enrolmentID)
        cur = conn.cursor()
        cur.execute(sql_cmd, values)
        if len(cur.fetchall()) > 0:
            return True
        else:
            return False


if __name__ == '__main__':
    enrolments = get_enrolments_list()
    e1 = enrolments[0]
    print(e1.id)
    print(e1.studentID)
    print(e1.student_name)
    print(e1.year_string)