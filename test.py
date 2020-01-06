import psycopg2

try:
   connection = psycopg2.connect(user="postgres",
                                  password="kobokobo",
                                  host="127.0.0.1",
                                  port="5432",
                                  database="postgres")
   cursor = connection.cursor()

   postgreSQL_select_Query = ""
   for i in range (6):
        for j in range (10):
        #j en x
        #i en y
            postgreSQL_select_Query  += "INSERT INTO public.capteur (id, x, y, intensite) VALUES (" + str(10*i+j) + ", " + str(j) + ", "+ str(i) +", 0); \n"

   # postgreSQL_select_Query = "select * from capteur; select * from capteur;"

   cursor.execute(postgreSQL_select_Query)
   """
   cursor.execute("select * from capteur")
   print("Selecting rows from mobile table using cursor.fetchall")
   mobile_records = cursor.fetchall() 
   
   print("Print each row and it's columns values")
   for row in mobile_records:
       print("Id = ", row[0], )
       print("x = ", row[1])
       print("y  = ", row[2])
       print("intensity = ", row[3],"\n")
    """
except (Exception, psycopg2.Error) as error :
    print ("Error while fetching data from PostgreSQL", error)

finally:
    #closing database connection.
    if(connection):
        cursor.close()
        connection.close()
        print("PostgreSQL connection is closed")