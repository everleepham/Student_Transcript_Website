import mysql.connector
from datetime import datetime


def connect(
    db_host: str = "localhost",
    db_port: int = 3245,
    db_user: str = "admin",
    db_password: str = "admin",
    db_name: str = "project",
) -> mysql.connector.connection.MySQLConnection:
    """
    Connects to the MySQL database
    :return: a connection object
    """
    conn = mysql.connector.connect(
        host=db_host, port=db_port, user=db_user, password=db_password, database=db_name
    )
    return conn


def format_date(datetime):
    return datetime.strftime("%d/%m/%Y")


def main():
    with open("./sites/welcome_page.html", "r") as file:
        html = file.read()

    with connect() as connection, connection.cursor() as cursor:
        cursor.execute(
            "select s.student_population_code_ref, count(s.student_epita_email) FROM students s group by s.student_population_code_ref  "
        )
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

    html = html.replace("%datetime%", format_date(datetime.now()))

    with open("./sites/index.html", "w") as file:
        file.write(html)

    print(f"Created {file}")


if __name__ == "__main__":
    main()
