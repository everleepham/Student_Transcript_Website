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

    cursor.close()
    connection.close()

for major in majors:
    new_file = f'./{major}.html'

    with open(original, 'r') as f:
        html = f.read()

    html = html.replace('%major%', major)

    with open('./sites/student_row_fragment.html', 'r') as file:
        students_rows_template = file.read()

    students_rows_html = ''

    
