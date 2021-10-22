from flask import jsonify

import psycopg2
import json
#se agrego un a linea de codigo para subir a github
class ConexionData:

    conexion = ''

    def conectar_base(self):
        try:
            credenciales = {
                "dbname": "ganado",
                "user": "postgres",
                "password": "Soypoderoso01",
                "host": "localhost",				
                "port": 5432
            }
            self.conexion = psycopg2.connect(**credenciales)
            if self.conexion :
                print('it works')
        except psycopg2.Error as e:
            print("Ocurrió un error al conectar a PostgreSQL: ", e)
    
    def insertar_datos(self,id,nombre,tipo,zona):
        try:
            print('Listo para insertar datos')
            data = []
            
            with self.conexion.cursor() as cursor:
                consulta = "INSERT INTO ANIMALES(NOMBRE,TIPO) VALUES (%s, %s);"                
                cursor.execute(consulta, (nombre, tipo)) 

                consulta = "SELECT MAX(ANI_ID) FROM ANIMALES;"
                cursor.execute(consulta, (nombre, tipo)) 
                objeto = cursor.fetchall()  
                          
                consulta = "INSERT INTO UBICACION_ANIMAL(ANI_ID,UBI_ID,CANTIDAD) VALUES (%s,%s, %s);"                
                cursor.execute(consulta, (objeto[0][0],zona, 1))          
                           
            self.conexion.commit()            

        except psycopg2.Error as e:
            print("Ocurrió un error al insertar: ", e)

    def retornar_animales(self):
        try:
            data = []            
            print('Listo para mostrar datos')
            with self.conexion.cursor() as cursor:
#Aqui se hace realiza un 
# query = " SELECT ANI_ID||'',NOMBRE,TIPO FROM ANIMALES;"
                query ="SELECT animales.ANI_ID||'',NOMBRE,animales.TIPO,ubi.ubi_id||'', ubi.tipo FROM ANIMALES animales left join ubicacion_animal ubi_animal on animales.ani_id= ubi_animal.ani_id left join ubicacion ubi on ubi_animal.ubi_id = ubi.ubi_id;"

                cursor.execute(query)                             
                objeto = cursor.fetchall()  
                #------------------------
                for animals in objeto:
                    data_got_db = {
                        'id' : animals[0],
                        'nombre' : animals[1],
                        'tipo' : animals[2],
                        'ubicacion' : animals[3]}
                    data.append(data_got_db)
                #-------------------                                                 
            self.conexion.close()
            return jsonify({'animals':data})  
        except psycopg2.Error as e:
            print("Ocurrió un error al retornar: ", e)

    def retornar_ubicacion(self):
        try:
            data = []
            print('Listo para mostrar datos')
            with self.conexion.cursor() as cursor:
                query = " SELECT UBI_ID||'',LATITUD||'',LONGITUD||'',TIPO FROM UBICACION;"            
                cursor.execute(query)               
                objeto = cursor.fetchall()
                   #------------------------
                for animals in objeto:
                    data_got_db = {
                        'id' : animals[0],
                        'latitud' : animals[1],
                        'longitud' : animals[2],
                        'tipo' : animals[3]}
                    data.append(data_got_db)
                #-------------------                
            self.conexion.close()
            return jsonify({'ubications':data}) 
        except psycopg2.Error as e:
            print("Ocurrió un error al retornar: ", e)


    def retornar_cantidad(self):
        try: 
            data = []        
            print('Listo para mostrar datos')
            with self.conexion.cursor() as cursor:
                query = " SELECT UBI.TIPO,COUNT(*) FROM UBICACION_ANIMAL UBI_ANI JOIN UBICACION UBI ON UBI_ANI.UBI_ID = UBI.UBI_ID GROUP BY UBI.TIPO;"            
                cursor.execute(query)               
                objeto = cursor.fetchall() 
                    #------------------------
                for animals in objeto:
                    data_got_db = {
                        'tipo' : animals[0],
                        'cuenta' : animals[1]}
                    data.append(data_got_db)
                #-------------------                  
            self.conexion.close()
            return jsonify({'qunatity':data})
        except psycopg2.Error as e:
            print("Ocurrió un error al retornar: ", e)


    


   


