import matplotlib.pyplot as plt
import mysql.connector
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



# Dữ liệu
sizes = [15, 30, 45, 10]
labels = ['CS', 'AIs', 'ISM', 'DSA', 'SE']
colors = ['gold', 'yellowgreen', 'lightcoral', 'lightskyblue']  # Các màu tương ứng với các phần

# Vẽ biểu đồ tròn
plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%')

# Hiển thị biểu đồ
plt.axis('equal')  # Đảm bảo biểu đồ tròn
plt.show()

