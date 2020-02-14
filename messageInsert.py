import threading
import ast
import csv
import json
import time
from datetime import date
import mysql.connector

mydb = mysql.connector.connect(
  host="motortale.cfpdw0gd4jhq.us-west-2.rds.amazonaws.com",
  user="motorboys",
  passwd="theonlymotorboys",
  database="motortale"
)

def crear_mensaje(multa, infraccion):
    mensaje_licencia = ""
    if multa["tieneLicenciaRetenida"]:
        mensaje_licencia = "Licencia retenida."

    print(multa["dominio"])    
    return "INSERT INTO todo (dominio, fecha, evento, lugar, descripcion, fecha_adicion ) VALUES ('" + multa["dominio"] + "', '" + time.strftime('%Y-%m-%d', time.localtime(multa["fechaEmision"]/1000)) + "', 'Infraccion', '" + multa["autoridadAplicacion"] + "', '" + str(infraccion["articulo"]) + " - " + infraccion["descripcion"] + " " + mensaje_licencia + "', '" + str(date.today()) + "');"
    

def guardar_mensaje(mensaje, filename):
    f = open("jsons_to_database/" + filename + ".sql", "a")
    f.write(mensaje + "\n")
    f.close()
    #print("Insertando: " + mensaje)
    #mycursor = mydb.cursor(buffered=True)
    #mycursor.execute(mensaje)
    #mydb.commit()


def nuevoProceso(filename):
    try:   
        f = open("jsons_to_database/" + filename + ".txt", "r")

        for x in f:
            if x[0] == filename[0] and int(x[7]) > 0:
                index = 9

                if str(x[8]).isnumeric():
                    index = 10
                if str(x[9]).isnumeric():
                    index = 11

                jsontext = x[index:].replace('"', '*').replace(" '", ' "').replace(" '", ' "').replace("':", '":').replace(" '", ' "').replace("',", '",').replace("'}", '"}').replace("{'", '{"').replace("True", "true").replace("False", "false").replace("None", '""').replace("accidentes,", "accidentes").replace("velocidad, distancia, tiempo", "velocidad distancia tiempo").replace("comportamiento,", "comportamiento").replace("\\xa0", "")
                multas_json = json.loads(jsontext)

                for multa in multas_json:

                    infracciones = json.loads(str(multa["infracciones"]).replace("'", '"'))

                    for infraccion in infracciones:
                        mensaje = crear_mensaje(multa, infraccion)
                        guardar_mensaje(mensaje, filename)
                    

        f.close()
    except Exception as e:
        f = open("jsons_to_database/errorlog.txt", "a")
        f.write(filename + str(e) + "\n")
        f.close()



def main():
    threads = list()

    iniciales = ['PA', 'PB', 'PC', 'PD', 'PE', 'PF', 'PG', 'PH', 'PI', 'PJ', 'PK', 'PL', 'PM', 'PN', 'PO', 'PP', 'PQ', 'PR', 'PS', 'PT', 'PU', 'PV', 'PW', 'PY', 'PX', 'PZ']

    for i in range(len(iniciales)):
        t = threading.Thread(target=nuevoProceso, args=(iniciales[i],))
        threads.append(t)
        t.start()

if __name__ == "__main__":
    main()