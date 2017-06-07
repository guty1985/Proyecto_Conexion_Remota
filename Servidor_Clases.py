#!/usr/bin/python
# -*- coding: utf-8 -*-


#Para que funcione se debe utlizar este comando en la consola python -m Pyro4.naming -n (direccion ip del equipo que sera servidor)

from __future__ import print_function
import Pyro4
from bs4 import BeautifulSoup
from requests import get
import json
import urllib
import MySQLdb
etiquetas_imagenes= list()
import re, string
import mysql.connector
import ast

HOST = '192.168.1.67'  # Dirrecion Ip donde se enuentra la Base de Datos
USER = 'root' # Usuario de la Base de Datos
PASSWORD = ''
DATABASE = 'paginas_web' #Nombre de la Base de Datos

@Pyro4.expose
class Servidor(object): # Clase Para invocar las funciones

    @property
    def conectar(self):
        try:
            conexion = mysql.connector.connect(host=HOST,   #Parametros para realizar la conexion a la Base de Datos
                                               database=DATABASE,
                                               user=USER,
                                               password=PASSWORD)

            cursor = conexion.cursor() #registros en el tiempo desde el servidor
            if cursor:
                #return True
                return "Conexion Exitosa"
        except mysql.connector.connect as e:
            return e

    def run_query(self, query):
        conexion = (HOST,USER,PASSWORD,DATABASE) #Parametros para hacer conexion a la Base de Datos

        conn = MySQLdb.connect(*conexion)  # Conectar a la base de datos
        cursor = conn.cursor()  # Crear un cursor registros en el tiempo desde el servidor
        cursor.execute(query)  # Se utiliza para Ejecutar una consulta en la Base de Datos

        if query.upper().startswith('SELECT'):#Extrae los resultados de la consulta que se realiza
            data = cursor.fetchall()  # Traer los resultados de un select
        else:
            conn.commit()  # Hacer efectiva la escritura de datos
            data = None

        cursor.close()  # Cerrar el cursor
        conn.close()  # Cerrar la conexión

        return data


# ---------Funciones del Cliente-----------
    @Pyro4.expose
    def validar_usuario(self,usuario): # Se validad si el usuario es Cliente o Adminsitrador
        if usuario == "Marcela":
            return (True)
        else:
            return (False)

    @Pyro4.expose
    def agregar_pagina(self,pagina):
        query = "INSERT INTO paginas (nombre)VALUES('%s')"%(pagina) # Consulta que se utiliza para insetar los datos a la Base de Datos
        self.run_query(query) #llama a la duncion run_query que se encarga de extaer los datos de la Base de Datos
        return ("Pagina Web Adicionada Satisfactoriamente")

    @property
    def listar_paginas(self):
        query = "SELECT * FROM paginas"# Consulta que se utiliza para listar los datos a la Base de Datos
        result = self.run_query(query)#llama a la Funcion run_query que se encarga de extaer los datos de la Base de Datos
        cadena = json.dumps(result)# json.dumps se encarga de tomar la consulta y volverla una lista(cadena)
        return (cadena)

    @Pyro4.expose
    def eliminar_pagina(self, pagina):
        query = "DELETE FROM paginas WHERE nombre ='%s'" % pagina # Consulta que se utiliza para listar los datos a la Base de Datos
        #SELECT numero FROM loteria WHERE numero = '%s'" % chance
        self.run_query(query)#llama a la Funcion run_query que se encarga de extaer los datos de la Base de Datos
        return ("Pagina Web Eliminada Satisfactoriamente")

    @Pyro4.expose
    def palabras(self, URL):
        recurso = get(URL)# get devuelve un valor para la clave dada
        texto = BeautifulSoup(recurso.text, 'html.parser').get_text() #Extrae el contenido Html de la Pagina y lo convierte en texto

        # Remplazo todos los caracteres ASCII de puntuacion por espacios e inicializa el Array
        palabrasArray = re.sub('[%s]' % re.escape(string.punctuation), ' ', texto).split() # re.escape especifica un conjunto de cadenas que coinciden con ella

        # Ordenacion sin repeticion de todos los elementos del Array
        numero = 0
        for i in sorted(set(palabrasArray)):
            # Imprime solo las palabras con caracteres alfabeticos.
            if (i.isalpha() == True): #isalpha() comprueba si la cadena se compone de sólo caracteres alfabéticos.
                numero += 1

        return (numero)

    @Pyro4.expose
    def diccionario(self, URL):
        query = "SELECT (pa_clave) FROM diccionario" # Consulta que se utiliza para insetar los datos a la Base de Datos
        result = self.run_query(query) #llama a la duncion run_query que se encarga de extaer los datos de la Base de Datos
        cadena = json.dumps(result)# json.dumps se encarga de tomar la consulta y volverla una lista(cadena)
        lista_1=[] #se crea una lista vacia
        lista_2=[]#se crea una lista vacia

        recurso = get(URL) #get devuelve un valor para la clave dada
        texto = BeautifulSoup(recurso.text, 'html.parser').get_text()#Extrae el contenido Html de la Pagina y lo convierte en texto

        # Remplazo todos los caracteres ASCII de puntuacion por espacios e inicializa el Array
        palabrasArray = re.sub('[%s]' % re.escape(string.punctuation), ' ', texto).split()# re.escape especifica un conjunto de cadenas que coinciden con ella

        # Ordenacion sin repeticion de todos los elementos del Array
        claves = ["Palabras que coinciden con el dicionario: "] #Crea lista
        for i in sorted(set(palabrasArray)):
            # Imprime solo las palabras con caracteres alfabeticos.
            if (i.isalpha() == True):#isalpha() comprueba si la cadena se compone de sólo caracteres alfabéticos.
                lista_1+=[i] #Se llema la lista

        lista = json.loads(cadena)
        for i in lista:
            lista_2+=(ast.literal_eval(json.dumps(i))) #se utiliza para quitar la u en el monento de la impresion
        con=0
        for j in lista_1: #Se reccore la lista
            for i in range(len(lista_2)):#Se reccore la lista
                if (lista_2[i] == j): #Compara el contenido de las lista
                    claves+=[j] #se concatena la variable clve con el contenido nuevo
                    con+=1

        if con > 0:
            return (claves)
        else:
            return (0)

    @Pyro4.expose
    def imagenes(self, URL):
        # URL = 'http://www.eltiempo.com/'  # Direccion de la Pagina Web
        recurso = get(URL)
        pagina = BeautifulSoup(recurso.text, 'html.parser')

        enlaces = pagina.find_all('img')  # Buscar Imagenes por medio de la etiqute img, find_all Devuelve una matriz que contiene todos los elementos del criterio ingresado
        for enlace in enlaces:
            etiquetas = enlace.get('alt')  # Nombre de la Imagen, texto alternativo
            if (etiquetas != None and etiquetas != ""):  # Seleciona las imagenes que tengan el argumento alt
                etiquetas_imagenes.append(etiquetas.upper())  # Concatena las imagenes en una lista

        a = len(etiquetas_imagenes) #len cuneta cuantos caracteres tiene una lista

        return (a)

    @Pyro4.expose
    def enlace_externo(self, pagina):
        url = pagina #recibe la pagina que envia el usuario
        recurso = get(url) # ya esta comentado en otras partes
        pagina = BeautifulSoup(recurso.text, 'html.parser')# ya esta comentado en otras partes
        con = 0

        links = pagina.find_all('a', attrs={'href': re.compile("http[s]?:")})# extrae todos los enlaces que se encuentren en la etiquet <a href y contegan el http o https
        for i in links:
            con += 1

        return (con)

    @Pyro4.expose
    def enlace_interno(self,pagina):

        url = pagina
        recurso = get(url)#comentado anteriormente
        pagina = BeautifulSoup(recurso.text, 'html.parser')#comentado anteriormente
        cont = 0
        links = pagina.find_all('a', attrs={'href': re.compile("/")})#comentado anteriormente
        for i in links:
            cont += 1
        return (cont)

    @Pyro4.expose
    def analizar_url(self,URL):
            recurso = get(URL) #comentado anteriormente
            if (recurso.status_code == 200):  # si l apagina existe devuelve un 200
                pagina = BeautifulSoup(recurso.text, 'html.parser')  # #comentado anteriormente

                titulo = (pagina.title.string)# extrae el tirulo que se encuntra dentro de la etiqueta tittle de la pagina

                meta_des = pagina.findAll(attrs={"name": "description"})#extrae el contenido que se encuntra dentro de la etiqueta meta seguido de los atrrs especificados
                descripcion = meta_des[0]['content'].encode('utf-8') #Extrae solo el texto de la consulta anterior

                meta_a = pagina.findAll(attrs={"name": "author"})#extrae el contenido que se encuntra dentro de la etiqueta meta seguido de los atrrs especificados
                autor = meta_a[0]['content'].encode('utf-8')#Extrae solo el texto(contenido) de la consulta anterior

                meta_cla = pagina.findAll(attrs={"name": "keywords"})#extrae el contenido que se encuntra dentro de la etiqueta meta seguido de los atrrs especificados
                p_clave = meta_cla[0]['content'].encode('utf-8')#Extrae solo el texto (contenido) de la consulta anterior

                imagen = self.imagenes(URL)#llama a la fucion  y recibe el parametro

                externos =self.enlace_externo(URL)#llama a la fucion  y recibe el parametro
                internos= self.enlace_interno(URL)#llama a la fucion  y recibe el parametro

                a = ("Titulo: "+ titulo) #se concatena
                b = ("Descripcion Pagina: "+ descripcion)#se concatena
                c = ("Palabras Claves: " + p_clave)#se concatena
                d = ("Imagenes: Hemos encontrado " +str(imagen)+ " imagenes en la pagina")#se concatena
                e = ("Enlaces: Internos "+str(internos))#se concatena
                f = ("         Externos " + str(externos))#se concatena
                g = ("Autor: "+ autor)#se concatena
                lista = [a,g,b,c,d,e,f]#se crea una lista con las concatenaciones de las variable anteriores

                return (lista)

    @Pyro4.expose
    def analizar_keywords(self,URL):
        recurso = get(URL)  # Tomar el codigo
        if (recurso.status_code == 200):  # Conexion
            pagina = BeautifulSoup(recurso.text, 'html.parser')  # Extrae el Html de la pagina

            meta_cla = pagina.findAll(attrs={"name": "keywords"})#explicado en la anterior
            p_clave = meta_cla[0]['content'].encode('utf-8')
            c = ("Palabras Claves: " + p_clave)
            return (c)

    @Pyro4.expose
    #Explicado en el diccionario hace los mismo
    def sociales(self,URL):
        recurso = get(URL)
        texto = BeautifulSoup(recurso.text, 'html.parser').get_text()

        # Remplazo todos los caracteres ASCII de puntuacion por espacios e inicializa el Array
        palabrasArray = re.sub('[%s]' % re.escape(string.punctuation), ' ', texto).split()

        # Ordenacion sin repeticion de todos los elementos del Array
        #numero = 0
        Redes=["Redes Sociales: "]
        lista =["Facebook","youtube","Twitter","Instagram"]
        for i in sorted(set(palabrasArray)):
            # Imprime solo las palabras con caracteres alfabeticos.
            if (i.isalpha() == True):
                for j in range(len(lista)):
                    if i == lista[j]:
                        Redes+=[i]

        return (Redes)

    # Explicado en el diccionario hace los mismo
    @Pyro4.expose
    def enlaza_pagina(self, URL):

        query = "SELECT (nombre) FROM paginas"
        result = self.run_query(query)
        cadena = json.dumps(result)
        lista = json.loads(cadena)
        lista_1=[]
        for i in lista:
            lista_1 += (ast.literal_eval(json.dumps(i)))

        recurso = get(URL)
        pagina = BeautifulSoup(recurso.text, 'html.parser')

        enlaces = pagina.find_all('a')  # Buscar enlaces por medio de la etiqute img
        for enlace in enlaces:
            etiquetas = enlace.get('href')  # Nombre de la etiqueta despues del a, texto alternativo
            if (etiquetas != None and etiquetas != ""):  # Seleciona los enlaces
                etiquetas_imagenes.append(etiquetas.upper())  # Concatena las enlaces en una lista

        con =0
        for j in etiquetas_imagenes:
            for i in range(len(lista_1)):
                if (lista_1[i] == j):
                    con +=1

        if con >0:
            return("Puntuacion Extra, Enlazar(Paginas Guardadas)")
        else:
            return ("No Obtuvo Puntuacion Extra, No Enlaza(Paginas Guardadas)")

    @Pyro4.expose
    def estructura_web(self,URL):
        recurso = get(URL)  # Tomar el codigo
        pagina = BeautifulSoup(recurso.text, 'html.parser')
        return (URL)


            # Explicado en el diccionario hace los mismo

    @Pyro4.expose
    def penalizar_pagina(self, URL):
        #pagina=(str(URL))
        query = "SELECT (palabra) FROM pa_no_apta"
        result = self.run_query(query)
        cadena = json.dumps(result)
        lista_1 = []
        lista_2 = []



        #lista = ["sexo", "Desnudo", "Denudas", "Porno", "xxx"]
        recurso = get(URL)
        texto = BeautifulSoup(recurso.text, 'html.parser').get_text()

        # Remplazo todos los caracteres ASCII de puntuacion por espacios e inicializa el Array
        palabrasArray = re.sub('[%s]' % re.escape(string.punctuation), ' ', texto).split()
        claves = ["Pagina web: " + str(URL) + " Penalizada (Contenido No Apto): "]
        # Ordenacion sin repeticion de todos los elementos del Array
        for i in sorted(set(palabrasArray)):
            # Imprime solo las palabras con caracteres alfabeticos.
            if (i.isalpha() == True):
                lista_1 += [i]

        lista = json.loads(cadena)
        for i in lista:
            lista_2 += (ast.literal_eval(json.dumps(i)))
        con = 0
        for j in lista_1:
            for i in range(len(lista_2)):
                # print (lista_2[i])
                if (lista_2[i] == j):
                    claves += [j]
                    con += 1

        if con > 0:
            query = "INSERT INTO penalizadas(pagina)VALUES('%s')" % (URL)
            self.run_query(query)

            return (claves)
        else:
            return (0)

    @Pyro4.expose
    def penalizar_reputacion(self,URL):
        query = "SELECT (pagina) FROM lista_negra"
        result = self.run_query(query)
        cadena = json.dumps(result)
        lista_1 = []
        lista_2 = []

        # lista = ["sexo", "Desnudo", "Denudas", "Porno", "xxx"]
        recurso = get(URL)
        texto = BeautifulSoup(recurso.text, 'html.parser').get_text()

        # Remplazo todos los caracteres ASCII de puntuacion por espacios e inicializa el Array
        palabrasArray = re.sub('[%s]' % re.escape(string.punctuation), ' ', texto).split()
        claves = ["Pagina web: " + str(URL) + " Penalizada (Contenido Dudosa Reputacion): "]
        # Ordenacion sin repeticion de todos los elementos del Array
        for i in sorted(set(palabrasArray)):
            # Imprime solo las palabras con caracteres alfabeticos.
            if (i.isalpha() == True):
                lista_1 += [i]

        lista = json.loads(cadena)
        for i in lista:
            lista_2 += (ast.literal_eval(json.dumps(i)))
        con = 0
        for j in lista_1:
            for i in range(len(lista_2)):
                # print (lista_2[i])
                if (lista_2[i] == j):
                    claves += [j]
                    con += 1

        if con > 0:
            return (claves)
        else:
            return (0)

    @Pyro4.expose
    def comprobar_enlaces(self, pagina):

        url = pagina
        lista=["Enlaces Externos"]
        recurso = get(url)
        pagina = BeautifulSoup(recurso.text, 'html.parser')


        for link in pagina.find_all(href=re.compile("http[s]?://")): #Explicado en paginas anteriores

            lista += [link.get('href')]# toma solo los valores especificos y los conveirte en texto para enviarlos en una lista

        return (lista)

    @Pyro4.expose
    #explicado en listar paginas
    def paginas_penalizadas(self):
        query = "SELECT * FROM penalizadas"
        result = self.run_query(query)
        cadena = json.dumps(result)
        return cadena

    # explicado en agregar  paginas
    @Pyro4.expose
    def ranking(self, titulo, pagina, externo, contenido, claves, interno, imagenes, aptas, longitud, redes, total):
    #def ranking(self,titulo,pagina,externos):
        query = "INSERT INTO ranking(titulo,pagina,externo,contenido,claves,interno,imagenes,no_penalizada,longitud,redes,total)VALUES('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')" % (titulo,pagina,externo,contenido,claves,interno,imagenes,aptas,longitud,redes,total)
        #query = "INSERT INTO ranking(titulo,pagina,externo)VALUES('%s','%s','%s')" % (titulo, pagina,externos)
        self.run_query(query)
        return "Pagina Web Adicionada Satisfactoriamente"

    @property
    # explicado en listar paginas
    def listar_ranking(self):
        query = "SELECT pagina FROM ranking ORDER BY total DESC"
        result = self.run_query(query)
        cadena = json.dumps(result)
        return (cadena)


    @property
    # explicado en listar paginas
    def listar_penalizadas(self):
        query = "SELECT * FROM penalizadas"
        result = self.run_query(query)
        cadena = json.dumps(result)
        return (cadena)


# ---------Funciones del Administrador-----------

    @Pyro4.expose
    # explicado en agregar  paginas
    def registro_empresas(self,empresa):
        query = "INSERT INTO empresas (nom_empresa)VALUES('%s')" % (empresa)
        self.run_query(query)
        return ("Empresa Registrada Satisfactoriamente")

    @Pyro4.expose
    # explicado en agregar  paginas
    def agregar_diccionario(self,palabra):
        query = "INSERT INTO diccionario (pa_clave)VALUES('%s')" % (palabra)
        self.run_query(query)
        return ("Plabaras Agregada Satisfactoriamente")

    @Pyro4.expose
    # explicado en agregar  paginas
    def palabras_malas(self,palabra):
        query = "INSERT INTO pa_no_aptas (palabra)VALUES('%s')" % (palabra)
        self.run_query(query)
        return ("Palabra Contenido Inadecuado Agregada Satisfactoriamente")


def main():
    #URL ="http://www.univision.com"
    Fernando = Servidor()
    #print (Fernando.estructura_web(URL))

    # Por ejemplo, accederemos al daemon y al servidor de nombres
    # Nosotros mismos y no usar servir Simple
    HOST_IP = "192.168.1.67" #Dirrecion IP del equipo servidor
    HOST_PORT = 9092 # Puerto donde escucha el servidor
    with Pyro4.Daemon(host=HOST_IP, port=HOST_PORT) as daemon:
        nasdaq_uri = daemon.register(Fernando)# Direccion Servidor de nombres
        #print(nasdaq_uri)
        with Pyro4.locateNS() as ns:
            ns.register("Marcela.Fernando.fernando", nasdaq_uri)# Registro Servidor de nombre
        print("Conexion Exitosa")

        daemon.requestLoop()


if __name__ == "__main__":
    main()
