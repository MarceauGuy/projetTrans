import psycopg2
from flask import Flask
from pprint import pprint



def getCapteur ():
    try:
        
        cursor = connection.cursor()

        postgreSQL_select_Query = "select * from capteur"
    
        cursor.execute(postgreSQL_select_Query)
        print("Selecting rows from mobile table using cursor.fetchall")
        mobile_records = cursor.fetchall() 
    
        print("Print each row and it's columns values")
        for row in mobile_records:
            print("Id = ", row[0], )
            print("x = ", row[1])
            print("y  = ", row[2])
            print("intensity = ", row[3],"\n")
        
    except (Exception, psycopg2.Error) as error :
        print ("Error while fetching data from PostgreSQL", error)
"""
    finally:
        #closing database connection.
        if(connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")
"""
def getCamion ():
    try:
        
        cursor = connection.cursor()

        postgreSQL_select_Query = "select idcamion, idcapteur, x, y, intensite from camion, typecamion where camion.idtype = typecamion.idtype;"
    
        cursor.execute(postgreSQL_select_Query)
        print("Selecting rows from mobile table using cursor.fetchall")
        mobile_records = cursor.fetchall() 
    
        print("Print each row and it's columns values")

        returnString=""
        for row in mobile_records:
            print("Id Camion = ", row[0], )
            print("Id Capteur = ", row[1])
            print("x  = ", row[2])
            print("y = ", row[3])
            print("intensite = ", row[4],"\n")
            returnString +=str(row[0]) + ","+ str(row[1]) + "," + str(row[2]) + "," + str(row[3]) + "," + str(row[4]) + ";" 

        print(returnString)    
        
    except (Exception, psycopg2.Error) as error :
        print ("Error while fetching data from PostgreSQL", error)
    return returnString
"""
    finally:
        #closing database connection.
        if(connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")
"""


###########################################################
###                   App                               ###
###########################################################

try:
    connection = psycopg2.connect(user="postgres",
                                        password="kobokobo",
                                        host="127.0.0.1",
                                        port="5432",
                                    database="postgres")
except (Exception, psycopg2.Error) as error :
    print ("Error while fetching data from PostgreSQL", error)

app = Flask(__name__)
@app.route("/")
def home():
    return "Hello, Flask!"


@app.route("/capteur")
def capteur ():
    getCapteur()
    return "on est alle chercher les capteurs"


@app.route("/camion")
def camion ():
    response = getCamion()
    return response

if __name__ == '__main__':
    app.run()