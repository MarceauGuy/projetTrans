import psycopg2
from flask import Flask, request, jsonify
from pprint import pprint
from psycopg2.extras import execute_values
import serial
import json
from flask_cors import CORS
#import paho.mqtt.publish as publish

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
    results = selectRequest("SELECT id, x, y, intensity FROM public.\"feuSimulated\" order by id;")
    #TODO : public.capteur
    returnString = ""
    for row in results:
        returnString +=  str(row[0]) + ","+ str(row[1]) + "," + str(row[2]) + "," + str(row[3]) + ";"
    returnString = returnString[:-1]
    #splitCapteurMqtt(returnString)
    return returnString


def getCamion ():
    returnString=""
    results = selectRequest("SELECT cam.idcamion, cam.x, cam.y, t.intensity, cam.idcapteur FROM public.camion cam, public.typecamion t, public.caserne cas where cam.idtype = t.idtype and cam.idcaserne = cas.idcaserne order by cam.idcamion;")
    for row in results : 
        returnString +=str(row[0]) + ","+ str(row[1]) + "," + str(row[2]) + "," + str(row[3]) + "," + (str(row[4]) if str(row[4]) != "None" else "-1" )+";"
    returnString = returnString[:-1]
    return returnString

def getFire():
    json_data = []
    returnString="["
    results = selectRequest("SELECT id, x, y, intensity FROM public.\"feuSimulated\" where intensity>0;")
    for row in results :
        returnString +="{\"id\":"+ str(row[0]) +",\"x\":"+ str(row[1]) +",\"y\":"+ str(row[2]) +",\"intensity\": "+ str(row[3]) +"},"
    returnString = returnString[:-1] +"]"
    if(len(returnString) == 1):
        returnString = "[]"
    return returnString

"""
SELECT idcamion, cam.x, cam.y FROM public.camion cam, public.caserne cas where cam.x != cas.x and cam.y != cas.y;
"""
def getMovingCamion():
    returnString = "["
    results = selectRequest("SELECT idcamion, cam.x, cam.y, t.intensity FROM public.camion cam, typecamion t where cam.idtype = t.idtype and (cam.x not in (select x from public.caserne) or cam.y not in (select y from public.camion));")
    for row in results :
        returnString +="{\"id\":"+ str(row[0]) +",\"x\":"+ str(row[1]) +",\"y\":"+ str(row[2]) +", \"intensity\":"+ str(row[3])+"},"
    returnString = returnString[:-1] +"]"
    if(len(returnString) == 1):
        returnString = "[]"
    return returnString

def getCaserne():
    returnString = "["
    results = selectRequest("SELECT idcaserne, x, y FROM public.caserne;")
    for row in results :
        returnString +="{\"id\":"+ str(row[0]) +",\"x\":"+ str(row[1]) +",\"y\":"+ str(row[2]) +"},"
    returnString = returnString[:-1] +"]"
    if(len(returnString) == 1):
        returnString = "[]"
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
    connection.commit()
    return "hehe"
    

def splitCapteur(capteurs) : 
    cursor = connection.cursor()
    queryString = """UPDATE public.capteur set intensity=%s where id=%s"""
    for capteur in capteurs:
        try:
            cursor.execute(queryString,(capteur['intensite'], capteur['id']))
        except (Exception, psycopg2.Error) as error :
            print ("Error while updating data in capteur table", error)   
    connection.commit()
    return "hehe"

def splitCapteurMqtt(message):
    capteurs = message.split(';')
    print("hehe")
    for capteur in capteurs:
        queryString = str(capteur) 
        publish.single("capteur", queryString, hostname="localhost")
        print("hehe")


def splitAffectation(affectations):
    splitAffectations = affectations.split(";")
    cursor = connection.cursor()
    queryString = """UPDATE public.camion SET  idcapteur=%s WHERE idcamion = %s;"""
    for affectation in splitAffectations:
        splitAffectation = affectation.split(",")
        if splitAffectation[1] == "-1":
            splitAffectation[1] = None
        try:
            cursor.execute(queryString,(splitAffectation[1], splitAffectation[0]))
        except (Exception, psycopg2.Error) as error :
            print ("Error while updating data in capteur table", error)   
    connection.commit()
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
CORS(app)

@app.route("/")
def home():
    return "Hello, Flask!"

@app.route("/map/getCapteurs")
def mapFire():
    response = getFire()
    return response

@app.route("/map/getCamions")
def mapCamion():
    response = getMovingCamion()
    return response

@app.route("/map/getCasernes")
def mapCaserne():
    response = getCaserne()
    return response

@app.route("/sensor/setCapteurs", methods=['POST'])
def sensorsCapteur():
    print(request.data)
    #print(json.loads(request.data)[0]["intensite"])
    #splitCapteur(json.loads(request.data))
    return "hehe"

@app.route("/capteur/getCapteurs", methods = ['GET'])
def fetchCapteur ():
    response = getCapteur()
    return response


@app.route("/read")
def readUART():
    x = ser.readline()

@app.route("/camion/getCamions", methods = ['GET'])
def fetchCamion ():
    response = getCamion()
    return response

@app.route("/camion/updateAffectation", methods=['POST'])
def fetchAffectation ():
    splitAffectation(request.data)
    return "fait"


    
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000, debug=True)