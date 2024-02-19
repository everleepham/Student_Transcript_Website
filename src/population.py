import mysql.connector
import os

majors = ['AIs', 'CS', 'ISM', 'DSA', 'SE']

# original_file = 'Population.html'

def connect(db_host: str, db_port: int, db_user: str, db_password: str, db_name: str) -> mysql.connector.connection.MySQLConnection:
    """
    Connects to the MySQL database
    :return: a connection object
    """
    conn = mysql.connector.connect(
        host=db_host,
        port=db_port,
        user=db_user,
        password=db_password,
        database=db_name
    )
    return conn

# TODO read those configuration entries from a configuration file
host = 'localhost'
port = 3245  
user = 'admin'
password = 'admin'
database_name = 'project'

for major in majors:

    html_file = f'./sites/populations/2021/fall/{major}.html'

    connection = connect(host, port, user, password, database_name)
    cursor = connection.cursor()

    cursor.execute(
        f"SELECT sub.STUDENT_EPITA_EMAIL, sub.CONTACT_FIRST_NAME, sub.CONTACT_LAST_NAME, "
        f"SUM(sub.COURSE_PASSED) AS PASSED, COUNT(sub.COURSE_PASSED) AS TOTAL "
        f"FROM (SELECT s.STUDENT_EPITA_EMAIL, c.CONTACT_FIRST_NAME, c.CONTACT_LAST_NAME, g.GRADE_COURSE_CODE_REF, "
        f"CASE WHEN ROUND(SUM(g.GRADE_SCORE*e.EXAM_WEIGHT)/SUM(e.EXAM_WEIGHT)) >= 10 "
        f"THEN 1 ELSE 0 END AS COURSE_PASSED "
        f"FROM STUDENTS s "
        f"INNER JOIN CONTACTS c ON s.STUDENT_CONTACT_REF = c.CONTACT_EMAIL "
        f"INNER JOIN GRADES g ON s.STUDENT_EPITA_EMAIL = g.GRADE_STUDENT_EPITA_EMAIL_REF "
        f"INNER JOIN EXAMS e ON g.GRADE_COURSE_CODE_REF = e.EXAM_COURSE_CODE "
        f"WHERE s.STUDENT_POPULATION_CODE_REF LIKE '{major}%' "
        f"GROUP BY s.STUDENT_EPITA_EMAIL, c.CONTACT_FIRST_NAME, c.CONTACT_LAST_NAME, g.GRADE_COURSE_CODE_REF) AS sub "
        f"GROUP BY sub.STUDENT_EPITA_EMAIL, sub.CONTACT_FIRST_NAME, sub.CONTACT_LAST_NAME"
    )

    # Store results of third query in a list
    data: list[tuple] = cursor.fetchall()

    cursor.execute(
       f"SELECT c.COURSE_CODE, c.COURSE_NAME, COUNT(*) AS session_count "
        f"FROM COURSES c "
        f"JOIN SESSIONS s ON c.COURSE_CODE = s.SESSION_COURSE_REF "
        f"JOIN PROGRAMS p ON c.COURSE_CODE = p.PROGRAM_COURSE_CODE_REF "
        f"WHERE p.PROGRAM_ASSIGNMENT LIKE '{major}%' "
        f"GROUP BY c.COURSE_CODE, c.COURSE_NAME"
    )

    value: list[tuple] = cursor.fetchall()

    # Close the cursor and connection
    cursor.close()
    connection.close()
    
    with open(html_file, 'r') as f:
        html = f.read()
    
    # html = html.replace('Population_Code', major)

    with open('./sites/student_row_fragment.html', 'r') as file:
        students_rows_template = file.read()  

    students_rows = ""

    for i, tup in enumerate(data):
        student_grade_href = f"./{tup[0]}_grade.html"   
        temp = students_rows_template.replace(r'%student_email%', tup[0])
        temp = temp.replace(r'%student_fname%', tup[1])
        temp = temp.replace(r'%student_lname%', tup[2])
        temp = temp.replace(r'%pass_count%', f'{tup[3]} / {tup[4]}')
        temp = temp.replace(r'%grades_href%', student_grade_href)
        students_rows += temp
    
    with open('./sites/course_row_fragment.html', 'r') as file:
        courses_rows_template = file.read()

    courses_rows = ""

    for i, tup in enumerate(value):
        temp = courses_rows_template.replace(r'%course_id%', tup[0])
        temp = temp.replace(r'%course_name%', tup[1])
        temp = temp.replace(r'%sessions_count%', tup[2])
        courses_rows += temp
    
    html = html.replace('%student_rows%', students_rows)
    html = html.replace("%courses_rows%", courses_rows)

    with open(html_file, 'w') as f: 
        f.write(html)

    print(f'Updated {file}')
