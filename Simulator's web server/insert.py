from pprint import pprint


string = ""
for i in range (6):
    for j in range (10):
        #j en x
        #i en y
        string  = "INSERT INTO public.capteur(id, x, y, intensity) VALUES ("+ str(10*i+j+1) +", "+ str(j) +", "+ str(i) +", 0);"
        print(string)
