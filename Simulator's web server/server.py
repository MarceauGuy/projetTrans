import psycopg2
from flask import Flask, request
from pprint import pprint
from psycopg2.extras import execute_values
import serial

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

def getFeux ():
    results = selectRequest("SELECT * FROM public.\"feuSimulated\" order by id;")
    returnString = ""
    for row in results:
        returnString +=  str(row[0]) + ","+ str(row[1]) + "," + str(row[2]) + "," + str(row[3]) + ";"
    returnString = returnString[:-1]
    return returnString


def getCamion ():
    returnString=""
    results = selectRequest("SELECT cam.idcamion, cam.x, cam.y, cas.x, cas.y, t.intensity, cam.idcapteur FROM public.camion cam, public.typecamion t, public.caserne cas where cam.idtype = t.idtype and cam.idcaserne = cas.idcaserne order by cam.idcamion;")
    for row in results : 
        returnString +=str(row[0]) + ","+ str(row[1]) + "," + str(row[2]) + "," + str(row[3]) + "," + str(row[4]) + "," + str(row[5]) + "," + (str(row[6]) if str(row[6]) != "None" else "-1" ) + ";"
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
@app.route("/")
def home():
    return "Hello, Flask!"


@app.route("/feu/getFeux", methods = ['GET'])
def fetchCapteur ():
    response = getFeux()
    return response

@app.route("/feu/setFeux", methods = ['POST'])
def setCapteur():
    message = splitCapteur(request.data)
    #sendUARTMessage(message)
    #sendUARTMessage("012345678901234567890123456789012345678901234567890123456789\n")
    return "pour set les capteur"

@app.route("/camion/getCamions", methods = ['GET'])
def fetchCamion ():
    response = getCamion()
    return response

@app.route("/camion/getAffectation", methods=['GET'])
def fetchAffectation ():
    result = getAffectation(request.args.get("id"))
    if(len(result) == 0):
        returnString = "-1"
    else:
        if str(result[0][0]) == "None":
            returnString = "-1"
        else:
            returnString = str(result[0][0])
    return returnString

@app.route("/camion/setCamions", methods = ['POST'])
def setCamion ():
    splitCamion(request.data)
    return "pour set les camions"

    
if __name__ == '__main__':
    initUART()
    app.run(host='127.0.0.1', port=8080, debug=True)