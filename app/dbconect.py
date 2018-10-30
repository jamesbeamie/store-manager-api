import psycopg2
import os

#local imports
from .dbqueris import queries

def dbcon():
    url = os.getenv('DATABASE_URL')
    #set connection
    con = psycopg2.connect(url)
    return con

def init_db():
    try:
        connection = dbcon()
        connection.autocommit = True

        #cursor activation
        curs = connection.cursor()
        for query in queries:
            curs.execute(query)
        connection.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print("Database connection error!")
        print(error)



