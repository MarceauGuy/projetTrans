import psycopg2
from flask import Flask
from pprint import pprint

"""
    finally:
        #closing database connection.
        if(connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")
"""

def getCapteur ():
    try:
        
        cursor = connection.cursor()

        postgreSQL_select_Query = "SELECT * FROM public.capteur;"
    
        cursor.execute(postgreSQL_select_Query)
        mobile_records = cursor.fetchall() 
        returnString = ""
        print(mobile_records)
        for row in mobile_records:
            returnString +=  str(row[0]) + ","+ str(row[1]) + "," + str(row[2]) + "," + str(row[3]) + ";"
        print returnString
        
    except (Exception, psycopg2.Error) as error :
        print ("Error while fetching data from PostgreSQL", error)
    returnString = returnString[:-1]
    return returnString


def getCamion ():
    try:
        
        cursor = connection.cursor()

        postgreSQL_select_Query = "SELECT cam.idcamion, cam.x, cam.y, cas.x, cas.y, t.intensite, cam.idcapteur FROM public.camion cam, public.typecamion t, public.caserne cas where cam.idtype = t.idtype and cam.idcaserne = cas.idcaserne;"
    
        cursor.execute(postgreSQL_select_Query)
        mobile_records = cursor.fetchall() 
    
        returnString=""
        for row in mobile_records:
            returnString +=str(row[0]) + ","+ str(row[1]) + "," + str(row[2]) + "," + str(row[3]) + "," + str(row[4]) + "," + str(row[5]) + "," + str(row[6]) + ";" 

        print(returnString)    
        
    except (Exception, psycopg2.Error) as error :
        print ("Error while fetching data from PostgreSQL", error)
    returnString = returnString[:-1]
    return returnString
"""
    finally:
        #closing database connection.
        if(connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")
"""

def splitCamion() : 

    return "eheh"


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


@app.route("/capteur/getCapteurs")
def capteur ():
    response = getCapteur()
    return response

@app.route("/capteur/setCapteur")
def setCapteur():
    return "pour set les capteur"

@app.route("/camion/getCamions", methods = ['GET'])
def camion ():
    response = getCamion()
    return response


@app.route("/camion/setCamions", methods = ['POST'])
def updateCamion ():
    return "pour set les camions"

    
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)