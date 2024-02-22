import mysql.connector
import os

names = ['Glick Albina', 'Corrio Ammie', 'Nicka Bette', 'Figeroa Bernardo', 'Pugh Blondell', 'Albares Cammy', 'Lindall Carmelina', 'Hollack Cecily', 'Bruschke Danica', 'Ahle Delmy', 'Dickerson Dominque', 'Foller Donette', 'Lipke Elza', 'Bowley Emerson', 'Ferencz Erick', 'Stenseth Ernie', 'Vocelka Francine', 'Rim Gladys', 'Vanausdal Jamal', 'Briddick Jina', 'Blackwood Kallie', 'Waycott Kanisha', 'Rulapaugh Kati', 'Caldarera Kiley', 'Marrier Kris', 
         'Gato Lai', 'Reitler Laurel', 'Dilliard Leota', 'Isenhower Lettie', 'Perin Lavera', 'Hochard Malinda', 'Amigon Minna', 'Mastella Marjory', 'Munns Myra', 'Parlato Moon', 'Royster Maryann', 'Fern Natalie', 'Ostrosky Rozella', 'Wieser Sage', 'Morasca Simona', 'Shinko Solange', 'Hoogland Tamar', 'Buvens Tawna', 'Mulqueen Timothy', 'Shields Tyra', 'Wenner Tonette', 'Inouye Veronika', 'Toelkes Viva', 'Giguere Wilda', 'Whobrey Yuki']


# Code that creates the names list:

"""

names_column = '''  # this column is copied from database
Glick Albina
Corrio Ammie
Nicka Bette
Figeroa Bernardo
...
Whobrey Yuki

'''

names_list = names_column.strip().split('\n')

print(names_list)

"""

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
    
        "select s.student_population_code_ref, s.student_epita_email, concat(c.contact_last_name, ' ', c.contact_first_name), s.student_population_period_ref, c.contact_birthdate "
        "from students s "
        "join contacts c "
        "on s.student_contact_ref  = c.contact_email "
        f"where concat(c.contact_last_name, ' ', c.contact_first_name) like '{name}' "
    ) #test

    data: list[tuple] = cursor.fetchall()

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

        if tup[0] == 'AIs':
            html = html.replace('%major%', 'AIs')
        elif tup[0] == 'CS':
            html = html.replace('%major%', 'CS')
        elif tup[0] == 'ISM':
            html = html.replace('%major%', 'ISM')
        elif tup[0] == 'DSA':
            html = html.replace('%major%', 'DSA')
        else:
            html = html.replace('%major%', 'SE')

    html = html.replace('%grade_rows%', grades_rows)

    with open(new_file, 'w') as f:
        f.write(html)

    print(f'Created {new_file}')

