import psycopg2
from flask import Flask, request
from pprint import pprint
from psycopg2.extras import execute_values
import serial
from flask_cors import CORS

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
    return returnString


def getCamion ():
    returnString=""
    results = selectRequest("SELECT cam.idcamion, cam.x, cam.y, t.intensity, cam.idcapteur FROM public.camion cam, public.typecamion t, public.caserne cas where cam.idtype = t.idtype and cam.idcaserne = cas.idcaserne order by cam.idcamion;")
    for row in results : 
        returnString +=str(row[0]) + ","+ str(row[1]) + "," + str(row[2]) + "," + str(row[3]) + "," + (str(row[4]) if str(row[4]) != "None" else "-1" )+";"
    returnString = returnString[:-1]
    return returnString

def getFire():
    returnString=""
    results = selectRequest("SELECT id, x, y, intensity FROM public.\"feuSimulated\" where intensity>0;")
    for row in results :
        returnString +=  str(row[0]) + ","+ str(row[1]) + "," + str(row[2]) + "," + str(row[3]) + ";"
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
    connection.commit()
    return "hehe"
    

def splitCapteur(capteurs) : 
    splitCapteurs = capteurs.split(";")
    cursor = connection.cursor()
    queryString = """UPDATE public.\"feuSimulated\" set intensity=%s where id=%s"""
    #TODO : public.capteur
    uartString = ""
    for capteur in splitCapteurs:
        splitCapteur = capteur.split(",")
        uartString+=splitCapteur[1]
        try:
            cursor.execute(queryString,(splitCapteur[1], splitCapteur[0]))
        except (Exception, psycopg2.Error) as error :
            print ("Error while updating data in capteur table", error)   
    connection.commit()
    return uartString

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

# send serial message 
# Don't forget to establish the right serial port ******** ATTENTION
# SERIALPORT = "/dev/ttyUSB0"
SERIALPORT = "/dev/tty2"
BAUDRATE = 115200
ser = serial.Serial()

def initUART():
    ser.port=SERIALPORT
    ser.baudrate=BAUDRATE
    ser.bytesize = serial.EIGHTBITS #number of bits per bytes
    ser.parity = serial.PARITY_NONE #set parity check: no parity
    ser.stopbits = serial.STOPBITS_ONE #number of stop bits
    ser.timeout = None          #block read

    # ser.timeout = 0             #non-block read
    # ser.timeout = 2              #timeout block read
    ser.xonxoff = False     #disable software flow control
    ser.rtscts = False     #disable hardware (RTS/CTS) flow control
    ser.dsrdtr = False       #disable hardware (DSR/DTR) flow control
    try:
        ser.open()
    except serial.SerialException:
        print("Serial {} port not available".format(SERIALPORT))
        exit()

def sendUARTMessage(msg):
    ser.write(msg.encode())
    # print("Message <" + msg + "> sent to micro-controller." )
     
            
app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
    return "Hello, Flask!"

@app.route("/map/getFire")
def mapRequest():
    response = getFire()
    return response


@app.route("/capteur/getCapteurs", methods = ['GET'])
def fetchCapteur ():
    response = getCapteur()
    return response

@app.route("/capteur/setCapteurs", methods = ['POST'])
def setCapteur():
    message = splitCapteur(request.data)
    #sendUARTMessage(message)
    #sendUARTMessage("012345678901234567890123456789012345678901234567890123456789")
    return "pour set les capteur"


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
    initUART()
    app.run(host='127.0.0.1', port=8000, debug=True)