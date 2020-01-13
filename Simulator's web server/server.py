import psycopg2
from flask import Flask, request
from pprint import pprint
from psycopg2.extras import execute_values
import serial
from Crypto import Random
from Crypto.Cipher import AES
import base64

"""
    finally:
        #closing database connection.
        if(connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")
"""

class Encryptor:
    def __init__(self, key):
        self.key = key

    def pad(self, s):
        return s + b"\0" * (AES.block_size - len(s) % AES.block_size)

    def encrypt(self, message, key, key_size=256):
        message = self.pad(message)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(key, AES.MODE_CBC, iv)
        return iv + cipher.encrypt(message)

    def decrypt(self, ciphertext, key):
        iv = ciphertext[:AES.block_size]
        cipher = AES.new(key, AES.MODE_CBC, iv)
        plaintext = cipher.decrypt(ciphertext[AES.block_size:])
        return plaintext.rstrip(b"\0")


def read_scales(message):
    key = 'nqbU0co8vJv5p/I6WHXNKLr9HXxXtewE'
    #b'[EX\xc8\xd5\xbfI{\xa2$\x05(\xd5\x18\xbf\xc0\x85)\x10nc\x94\x02)j\xdf\xcb\xc4\x94\x9d(\x9e'
    enc = Encryptor(key)
    clear = lambda: os.system('cls')

    #data = enc.encrypt(chn,key,128)
    data_send = enc.encrypt(message,key,128)
    print('data non chiffre:',message)

    base64_enc = base64.b64encode(data_send)
    #data_send = repr(data_send)
    #print(data.encode("hex"))
    print('data chiffre:',base64_enc )
    print('P1:',base64_enc[0:54] )
    print('P2:',base64_enc[54:108] )
    sendUARTMessage(base64_enc)


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
SERIALPORT = "/dev/ttyS3"
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
    ser.write(msg)
    print("Message <" + msg + "> sent to micro-controller." )
     
            
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
    read_scales(message)
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