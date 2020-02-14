import threading
import urllib.request
import json 
from time import gmtime, strftime
import pyodbc 

def nuevoProceso(inicial):
    try:
        msconn = pyodbc.connect('Driver={SQL Server Native Client 11.0};'
                        'Server=motortalems.cfpdw0gd4jhq.us-west-2.rds.amazonaws.com;'
                        'Database=motortale;'
                        'UID=motortale;'
                        'PWD=motortale01;'
                        'Integrated_Security=false;'
                        'Trusted_Connection=no;')

        while True:
            mycursor = msconn.cursor()
            mycursor.execute("exec sp_tpatentes_no_consultadas '" + inicial + "'")
            dominio = mycursor.fetchall()[0][0]

            if  dominio is None:
                break
        
            msconn.commit()
            
            contents = json.loads(urllib.request.urlopen("https://infraccionesba.gba.gob.ar/rest/consultar-infraccion?dominio=" + dominio).read())
            
            f = open("jsons/" + dominio[0] + "/" + dominio[0] + dominio[1] + ".txt", "a")
            f.write(dominio + ";" + str(contents["tieneInfracciones"]) + ";" + str(contents["infracciones"]) + "\n")
            f.close()
            
            print(dominio)
    except Exception as e:
        f = open("errorlog.txt", "a")
        f.write(inicial + str(e) + "\n")
        f.close()
        nuevoProceso(inicial)


def main():
    threads = list()
    primeras = ['G', 'H']#['M','N','O','P','I','J','K','L','E','F','G','H','A','B','C','D','R','S','T','U','V','W','X','Y','Z']
    segundas = ['M','N','O','P','I','J','K','L','E','F','G','H','A','B','C','D','R','S','T','U','V','W','X','Y','Z']
    iniciales = []

    for primera in primeras:
        for segunda in segundas:
            iniciales.append('' + primera + segunda + '')
    
    print(len(iniciales))

    for i in range(len(iniciales)):
        t = threading.Thread(target=nuevoProceso, args=(iniciales[i],))
        threads.append(t)
        t.start()

if __name__ == "__main__":
    main()