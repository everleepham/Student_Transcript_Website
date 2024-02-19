import mysql.connector
import os

names = ['Honeywell Arlette', 'Glick Albina', 'Slusarski Alisha', 'Iturbide Allene', 'Maclead Abel', 'Monarrez Amber',
         'Corrio Ammie', 'Venere Art', 'Sergi Alishia', 'Bolognia Brock', 'Nicka Bette', 'Figeroa Bernardo', 'Malet Blair',
          'Pugh Blondell', 'Rhym Bobbye', 'Albares Cammy', 'Vanheusen Carma' ]

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