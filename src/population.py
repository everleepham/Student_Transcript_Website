import mysql.connector
import os


majors = ['AIs', 'CS', 'ISM', 'DSA', 'SE']

original = 'populations.html'

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

host = 'localhost'
port = 3245  
user = 'admin'
password = 'admin'
database_name = 'project'

for major in majors:
    new_file = f'./{major}.html'

    connection = connect(host, port, user, password, database_name)
    cursor = connection.cursor()

    cursor.execute(
        "SELECT DISTINCT concat(c.contact_last_name, ' ', c.contact_first_name) as 'full name', c.contact_email, c.contact_first_name, c.contact_address, c.contact_city FROM contacts c"
    ) #test

    data: list[tuple] = cursor.fetchall()

    cursor.execute()

    value: list[tuple] = cursor.fetchall()

    cursor.close()
    connection.close()

for major in majors:
    new_file = f'./{major}.html'

    with open(original, 'r') as f:
        html = f.read()

    html = html.replace('%major%', major)

    with open('./sites/student_row_fragment.html', 'r') as file:
        students_rows_fragment = file.read()

    students_rows = ''

    for i, tup in enumerate(data):
        fullname = tup[3].replace(' ', '_')
        student_grade_href = f"./{fullname}.html"   
        temp = students_rows_fragment.replace(r'%grades_href%', student_grade_href)
        temp = temp.replace(r'%student_email%', tup[0])
        temp = temp.replace(r'%student_fname%', tup[1])
        temp = temp.replace(r'%student_lname%', tup[2])
        temp = temp.replace(r'%student_fullname%', tup[3])
        temp = temp.replace(r'%pass_count%', f'{tup[4]} / {tup[5]}')
        students_rows += temp

    with open('./sites/course_row_fragment.html', 'r') as file:
        courses_rows_fragment = file.read()
    
    courses_row = ''

    for i, tup in enumerate(value):
        temp = courses_rows_fragment.replace(r'%course_id%', tup[0])
        temp = temp.replace(r'%course_name%', tup[1])
        temp = temp.replace(r'%sessions_count%', tup[2])
        courses_row += temp

    html = html.replace('%student_rows%', students_rows)
    html = html.replace("%courses_rows%", courses_row)

    with open(new_file, 'w') as f: 
        f.write(html)

    print(f'Created {new_file}')
    
