import psycopg2
from flask import Flask, request
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
    returnString = ""
    try:
        
        cursor = connection.cursor()

        postgreSQL_select_Query = "SELECT * FROM public.capteur;"
    
        cursor.execute(postgreSQL_select_Query)
        mobile_records = cursor.fetchall() 
        
        print(mobile_records)
        for row in mobile_records:
            returnString +=  str(row[0]) + ","+ str(row[1]) + "," + str(row[2]) + "," + str(row[3]) + ";"
        print(returnString)
        
    except (Exception, psycopg2.Error) as error :
        print ("Error while fetching data from PostgreSQL", error)
    returnString = returnString[:-1]
    return returnString


def getCamion ():
    returnString=""
    try:
        
        cursor = connection.cursor()

        postgreSQL_select_Query = "SELECT cam.idcamion, cam.x, cam.y, cas.x, cas.y, t.intensite, cam.idcapteur FROM public.camion cam, public.typecamion t, public.caserne cas where cam.idtype = t.idtype and cam.idcaserne = cas.idcaserne;"
    
        cursor.execute(postgreSQL_select_Query)
        mobile_records = cursor.fetchall() 
    
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

def splitCamion(camions) : 
    queryString=""
    splitCamions = camions.split(";")
    cursor = connection.cursor()
    for camion in splitCamions:
        splitCamion = camion.split(",")
        try:
            cursor.execute("UPDATE public.camion SET x=%s, y=%s  where idcamion = %s",(splitCamion[1],splitCamion[2],splitCamion[0]))
        except (Exception, psycopg2.Error) as error :
            print ("Error while updating data in camion table", error)   
    return "hehe"
    


###########################################################
###                   App                               ###
###########################################################

try:
    connection = psycopg2.connect(user="postgres",
                                        password="tp",
                                        host="127.0.0.1",
                                        port="5432",
                                    database="postgres")


except (Exception, psycopg2.Error) as error :
    print ("Error while fetching data from PostgreSQL", error)

app = Flask(__name__)
@app.route("/")
def home():
    return "Hello, Flask!"


@app.route("/capteur/getCapteurs", methods = ['GET'])
def fetchCapteur ():
    response = getCapteur()
    return response

@app.route("/capteur/setCapteur", methods = ['POST'])
def setCapteur():
    print(request.data)
    return "pour set les capteur"

@app.route("/camion/getCamions", methods = ['GET'])
def fetchCamion ():
    response = getCamion()
    return response


@app.route("/camion/setCamions", methods = ['POST'])
def setCamion ():
    splitCamion(request.data)
    return "pour set les camions"

    
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)