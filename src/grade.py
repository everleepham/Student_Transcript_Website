import mysql.connector
from datetime import datetime
import os

names = ['Albina Glick', 'Ammie Corrio', 'Bette Nicka', 'Bernardo Figeroa', 'Blondell Pugh', 'Cammy Albares', 'Carmelina Lindall', 'Cecily Hollack', 'Danica Bruschke', 'Delmy Ahle', 'Dominque Dickerson', 'Donette Foller', 'Elza Lipke', 'Emerson Bowley', 'Erick Ferencz', 'Ernie Stenseth', 'Francine Vocelka', 'Gladys Rim', 'Jamal Vanausdal', 'Jina Briddick', 'Kallie Blackwood', 'Kanisha Waycott', 'Kati Rulapaugh', 'Kiley Caldarera', 'Kris Marrier', 'Lai Gato', 
         'Laurel Reitler', 'Leota Dilliard', 'Lettie Isenhower', 'Lavera Perin', 'Malinda Hochard', 'Minna Amigon', 'Marjory Mastella', 'Myra Munns', 'Moon Parlato', 'Maryann Royster', 'Natalie Fern', 'Rozella Ostrosky', 'Sage Wieser', 'Simona Morasca', 'Solange Shinko', 'Tamar Hoogland', 'Tawna Buvens', 'Timothy Mulqueen', 'Tyra Shields', 'Tonette Wenner', 'Veronika Inouye', 'Viva Toelkes', 'Wilda Giguere', 'Yuki Whobrey']


"""

names_column = '''  # this column is copied from database
Albina Glick
Ammie Corrio
Bette Nicka
Bernardo Figeroa
Blondell Pugh
...
Whobrey Yuki

'''

names_list = names_column.strip().split('\n')

print(names_list)

"""

intake_mapping = {
    'FALL': 'F2020',
    'SPRING': 'S2021'
}

original = '.\sites\grades.html'

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


for name in names:
    new_name = name.replace(' ','_')
    new_file = f"./sites/grade_html/{new_name}.html"

    connection = connect(host, port, user, password, database_name)
    cursor = connection.cursor()

    cursor.execute(
        "select s.student_population_code_ref, s.student_epita_email, concat(c.contact_first_name, ' ', c.contact_last_name), s.student_population_period_ref, c.contact_birthdate "
        "from students s "
        "join contacts c "
        "on s.student_contact_ref  = c.contact_email "
        f"where concat(c.contact_first_name, ' ', c.contact_last_name) like '{name}' "
    ) #test

    data = cursor.fetchall()

    cursor.close()
    connection.close()

    new_file = f"./sites/grade_html/{new_name}.html"

    
    with open(original, 'r') as f:
        html = f.read()

    html = html.replace("%full_name%", name)

    with open('./sites/grade_row_fragment.html', 'r') as file:
        grades_row_fragment = file.read()
    
    grades_rows = ""

    for i, tup in enumerate(data):
        temp = grades_row_fragment.replace(r'%student_major%', tup[0])
        temp = temp.replace(r'%student_email%', tup[1])
        temp = temp.replace(r'%student_fullname%', tup[2])
        temp = temp.replace(r'%course_id%', tup[3])
        temp = temp.replace(r'%grade', str(tup[4]))
        grades_rows += temp

    current_datetime = datetime.now()
    formatted_datetime = current_datetime.strftime('%d/%m/%Y')

    html = html.replace('%datetime%', formatted_datetime)

    html = html.replace('%major%', tup[0])
    html = html.replace('%intake%', intake_mapping.get(tup[3]))
    html = html.replace('%grade_rows%', grades_rows)

    with open(new_file, 'w') as f:
        f.write(html)

    print(f'Created {new_file}')
