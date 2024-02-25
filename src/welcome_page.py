import mysql.connector
import os

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

with open('./sites/index.html', 'r') as file:
    html = file.read()

connection = connect(host, port, user, password, database_name)
cursor = connection.cursor()

cursor.execute("select s.student_population_code_ref, count(s.student_epita_email) FROM students s group by s.student_population_code_ref  ")
pop_data = cursor.fetchall()

cursor.execute(
    "select s.student_population_code_ref, "
    "round(sum(a.attendance_presence) / count(*) * 100) as percentage "
    "from attendance a "
    "join students s "
    "on a.attendance_student_ref = s.student_epita_email "
    "group by s.student_population_code_ref "
)

att_data = cursor.fetchall()


for course, value in pop_data:
    placeholder = f"(%pop_{course.lower()}%)" 
    html = html.replace(placeholder, str(value))


for att, value in att_data:
    placeholder = f"(%att_{att.lower()}%)" 
    html = html.replace(placeholder, str(value))

with open('./sites/draft.html', 'w') as file:
    file.write(html)

print(f"Created {file}")