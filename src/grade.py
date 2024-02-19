import mysql.connector
import os

emails = ['albina.glick@epita.fr', 'ammie.corrio@epita.fr', 'bette.nicka@epita.fr', 'bernardo.figeroa@epita.fr', 
          'blondell.pugh@epita.fr', 'cammy.albares@epita.fr', 'carmelina.lindall@epita.fr', 'cecily.hollack@epita.fr',
          'danica.bruschke@epita.fr', ...]

# original_file = 'Population.html'

def connect(db_url: str, db_user: str, db_password: str) -> mysql.connector.connection.MySQLConnection:
    """
    connects to the MySQL database
    :return: a connection object
    """
    conn = mysql.connector.connect(
        host=db_url,
        user=db_user,
        password=db_password
    )
    return conn

# TODO read those configuration entries from a configuration file
url: str = 'jdbc:mysql://localhost:3245/project'
user: str = 'admin'
password: str = 'admin'
database_name: str = 'project'