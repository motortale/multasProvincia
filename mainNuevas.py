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
            mycursor.execute("exec sp_tpatentes_no_consultadas_nuevas '" + inicial + "'")
            dominio = mycursor.fetchall()[0][0]

            if  dominio is None:
                break
        
            msconn.commit()
            
            contents = json.loads(urllib.request.urlopen("https://infraccionesba.gba.gob.ar/rest/consultar-infraccion?dominio=" + dominio).read())
            
            f = open("jsons_nuevas/" + dominio[5] + "/" + dominio[5] + dominio[6] + ".txt", "a")
            f.write(dominio + ";" + str(contents["tieneInfracciones"]) + ";" + str(contents["infracciones"]) + "\n")
            f.close()
            
            print(dominio)
    except:
        nuevoProceso(inicial)


def main():
    threads = list()

    iniciales = ['AA', 'AB', 'AC', 'AD']
    numeros = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

    principios = []

    for inicial in iniciales:
        for num in numeros:
            principios.append('' + inicial + num + '')
    
    print(len(principios))

    for i in range(len(principios)):
        t = threading.Thread(target=nuevoProceso, args=(principios[i],))
        threads.append(t)
        t.start()

if __name__ == "__main__":
    main()