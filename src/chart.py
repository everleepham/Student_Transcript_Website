import matplotlib.pyplot as plt
import mysql.connector
import numpy as np
import os


def connect(
    db_host: str, db_port: int, db_user: str, db_password: str, db_name: str
) -> mysql.connector.connection.MySQLConnection:
    """
    Connects to the MySQL database
    :return: a connection object
    """
    conn = mysql.connector.connect(
        host=db_host, port=db_port, user=db_user, password=db_password, database=db_name
    )
    return conn


host = "localhost"
port = 3245
user = "admin"
password = "admin"
database_name = "project"

connection = connect(host, port, user, password, database_name)
cursor = connection.cursor()

cursor.execute(
    "select s.student_population_code_ref, "
    "(count(s.student_epita_email) / (select count(*) from students s)) * 100 as percentage "
    "FROM students s "
    "group by s.student_population_code_ref "
)

pop_percentage = cursor.fetchall()

cursor.execute(
    "select s.student_population_code_ref, "
    "round(sum(a.attendance_presence) / count(*) * 100) as percentage "
    "from attendance a "
    "join students s "
    "on a.attendance_student_ref = s.student_epita_email "
    "group by s.student_population_code_ref "
)

att_percentae = cursor.fetchall()


cursor.close()
connection.close()


# pie chart
size = []
labels = []

for tup in pop_percentage:
    size.append(tup[1])
    labels.append(tup[0])


colors = ['plum', 'cornflowerblue','lightpink', 'mediumaquamarine', 'navajowhite',]

plt.pie(size, labels=labels, colors=colors, autopct='%1.1f%%', textprops={'fontsize': 11})

plt.rcParams['font.size'] = 13

plt.axis('equal') 
plt.title('Populations', pad=20)
plt.savefig('sites/population.png')
plt.show()
plt.close()


# bar chart
categories = []
values = []

for tup in att_percentae:
    categories.append(tup[0])
    values.append(tup[1])

width = 0.5  

plt.bar(categories, values, color=colors, width=width)

for i in range(len(categories)):
    plt.text(i, float(values[i]) + 0.1, f"{str(values[i])}%", ha='center')

plt.xlabel('Majors')
plt.ylabel('Attendance percentage')
plt.title('Overall attendance', pad=20)

plt.savefig('sites/attendance.png')
plt.show()

plt.close()