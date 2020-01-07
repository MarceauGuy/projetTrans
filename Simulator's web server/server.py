import psycopg2
from flask import Flask, request
from pprint import pprint
from psycopg2.extras import execute_values

"""
    finally:
        #closing database connection.
        if(connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")
"""

def selectRequest(queryString):
    mobile_records = ""
    try:
        
        cursor = connection.cursor()
    
        cursor.execute(queryString)
        mobile_records = cursor.fetchall() 
        
    except (Exception, psycopg2.Error) as error :
        print ("Error while fetching data from PostgreSQL", error)
    return mobile_records   

def getCapteur ():
    results = selectRequest("SELECT * FROM public.capteur;")
    returnString = ""
    for row in results:
        returnString +=  str(row[0]) + ","+ str(row[1]) + "," + str(row[2]) + "," + str(row[3]) + ";"
    returnString = returnString[:-1]
    return returnString


def getCamion ():
    returnString=""
    results = selectRequest("SELECT cam.idcamion, cam.x, cam.y, cas.x, cas.y, t.intensite, cam.idcapteur FROM public.camion cam, public.typecamion t, public.caserne cas where cam.idtype = t.idtype and cam.idcaserne = cas.idcaserne;")
    for row in results : 
        returnString +=str(row[0]) + ","+ str(row[1]) + "," + str(row[2]) + "," + str(row[3]) + "," + str(row[4]) + "," + str(row[5]) + "," + str(row[6]) + ";"
    returnString = returnString[:-1]
    return returnString

def splitCamion(camions) : 
    splitCamions = camions.split(";")
    cursor = connection.cursor()
    queryString = """UPDATE public.camion SET x=%s, y=%s  where idcamion = %s"""
    for camion in splitCamions:
        splitCamion = camion.split(",")
        try:
            cursor.execute(queryString,(splitCamion[1],splitCamion[2],splitCamion[0]))
        except (Exception, psycopg2.Error) as error :
            print ("Error while updating data in camion table", error)   
    return "hehe"
    

def splitCapteur(capteurs) : 
    splitCapteurs = capteurs.split(";")
    cursor = connection.cursor()
    queryString = """UPDATE public.capteur set intensity=%s where id=%s"""
    for capteur in splitCapteurs:
        splitCapteur = capteur.split(",")
    try:
        cursor.execute(queryString,(splitCapteur[1], splitCapteur[0]))
    except (Exception, psycopg2.Error) as error :
        print ("Error while updating data in capteur table", error)   
    return "hehe"
    

def getAffectation(idCamion):
    queryString = "select idcapteur from public.camion where idcamion = "+idCamion+";"
    result = selectRequest(queryString)
    return result



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

@app.route("/capteur/setCapteurs", methods = ['POST'])
def setCapteur():
    print(request.data)
    splitCapteur(request.data)
    # TO DO: ecrire uart0
    return "pour set les capteur"

@app.route("/camion/getCamions", methods = ['GET'])
def fetchCamion ():
    response = getCamion()
    return response

@app.route("/camion/getAffectation", methods=['GET'])
def fetchAffectation ():
    print(request.args.get("id"))
    result = getAffectation(request.args.get("id"))
    if(len(result) == 0):
        returnString = "-1"
    else:
        returnString = str(result[0][0])
    return returnString

@app.route("/camion/setCamions", methods = ['POST'])
def setCamion ():
    splitCamion(request.data)
    return "pour set les camions"

    
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)