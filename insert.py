import mysql.connector
from mysql.connector import Error
from mysql.connector import errorcode
message = "To Kalanki"
try:
    connection = mysql.connector.connect(host="localhost",
                                          database="Hackathon",
                                          user="root",
                                          password="")
    mySql_insert_query = ("""INSERT INTO location(address) VALUES(%s)""", (message,))


    cursor = connection.cursor()
    cursor.execute(*mySql_insert_query)
    connection.commit()
    print(cursor.rowcount, "Record inserted successfully into Location")
    cursor.close()

except mysql.connector.Error as error:
    print("Failed to insert record into Location {}".format(error))

finally:
    if (connection.is_connected()):
        connection.close()
        print("MySQL connection is closed")
