import mysql.connector
import os

names = ['Honeywell Arlette', 'Glick Albina', 'Slusarski Alisha', 'Iturbide Allene', 'Maclead Abel', 'Monarrez Amber', 'Corrio Ammie', 'Venere Art', 'Sergi Alishia', 'Bolognia Brock', 'Nicka Bette', 'Figeroa Bernardo', 'Malet Blair', 'Pugh Blondell', 'Rhym Bobbye', 'Albares Cammy', 'Vanheusen Carma', 'Lindall Carmelina', 'Hollack Cecily', 'Caudy Chanel', 'Gibes Cory', 'Bruschke Danica', 'Juhas Deeanna', 'Crupi Delisa', 'Ahle Delmy', 'Chickering Devorah', 'Oldroyd Dyan', 'Dickerson Dominque', 'Foller Donette', 'Morocco Elly', 'Benimadho Elvera', 'Lipke Elza', 'Bowley Emerson', 'Ferencz Erick', 'Stenseth Ernie', 'Chui Ezekiel', 'Flosi Fletcher', 'Vocelka Francine', 'Saylors Fatima', 'Rim Gladys', 'Ruta Graciela', 'Eroman Ilene', 'Vanausdal Jamal', 'Butt James', 'Briddick Jina', 'Abdallah Johnetta', 'Stockham Jose', 'Darakjy Josephine', 'Blackwood Kallie', 'Waycott Kanisha', 'Klonowski Karl', 'Rulapaugh Kati', 'Caldarera Kiley', 'Marrier Kris', 'Gato Lai', 'Reitler Laurel', 'Dilliard Leota', 'Isenhower Lettie', 'Centini Lisha', 'Nestle Lorrie', 'Paprocki Lenna', 'Perin Lavera', 'Hochard Malinda', 'Poquette Mattie', 'Yglesias Maurine', 'Garufi Meaghan', 'Rhymes Micaela', 'Amigon Minna', 'Tollner Mitsue', 'Mastella Marjory', 'Munns Myra', 'Parlato Moon', 'Royster Maryann', 'Fern Natalie', 'Weight Penney', 'Campain Roxane', 'Ostrosky Rozella', 'Uyetake Sabra', 'Wieser Sage', 'Seewald Shenika', 'Morasca Simona', 'Shinko Solange', 'Barfield Stephaine', 'Emigh Stephen', 'Hoogland Tamar', 'Buvens Tawna', 'Mulqueen Timothy', 'Shields Tyra', 'Wardrip Tammara', 'Wenner Tonette', 'Gillian Valentine', 'Inouye Veronika', 'Toelkes Viva', 'Mondella Vallie', 'Giguere Wilda', 'Kolmetz Willard', 'Kusko Willow', 'Schemmer Youlanda', 'Whobrey Yuki']

# Code to create the names list:

"""
names_column = '''
Honeywell Arlette
Glick Albina
Slusarski Alisha
Iturbide Allene
Maclead Abel
...
Whobrey Yuki

'''

names_list = names_column.strip().split('\n')

print(names_list)

"""


original = 'grades.html'

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
    new_file = f'./{name}.html'

    connection = connect(host, port, user, password, database_name)
    cursor = connection.cursor()

    cursor.execute()

    data: list[tuple] = cursor.fetchall()

    cursor.close()
    connection.close()


for name in names:

    new_file = f'./{name}.html'

    with open(original, 'r') as f:
        html = f.read()

    html = html.replace("%full_name%", names)

    