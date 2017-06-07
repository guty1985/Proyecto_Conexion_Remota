#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import print_function
import json
import ast
from requests import get
from bs4 import BeautifulSoup
import Pyro4
@Pyro4.expose
class Cliente(object):
    def __init__(self):
        self.fernando =set()

def conexion():
    with Pyro4.locateNS() as ns:
        for marcela, url in ns.list(prefix="Marcela.Fernando.").items():
            thing = Pyro4.Proxy(url)

            usuario = (raw_input("Digite Usuario: "))
            condicion =(thing.validar_usuario(usuario))

            if (condicion == False):
                while condicion == False:
                    print("------------------------------------------")
                    print("\t\tMENU CLIENTE\t\t")
                    print("(1). Agregar Pagina Web ")
                    print("(2). Listar Paginas Web ")
                    print("(3). Eliminar Pagina Web ")
                    print("(4). Información SEO Pagina Web ")
                    print("(5). Ranking (Sitios - Criterios ")
                    print("(6). Listado de páginas penalizadas ")
                    print("(7). Salir")
                    op =int(raw_input("Digite una Opción: "))
                    repetir = "S"
                    #print(thing.conectar)
                    if (op == 1):
                        while repetir == "S" or repetir == "s":
                            pagina = (raw_input("Ingrese Pagina Web: "))
                            cadena = "http://" + str(pagina)
                            print(thing.agregar_pagina(cadena))
                            repetir = (raw_input("Desea Adiccionar Otra Pagina Web (S/N) "))

                    if (op == 2):
                        paginas = (thing.listar_paginas)
                        lista = json.loads(paginas)
                        for i in lista:
                            print(ast.literal_eval(json.dumps(i)))

                    if (op == 3):
                        paginas = (thing.listar_paginas)
                        lista = json.loads(paginas)
                        for i in lista:
                            print(ast.literal_eval(json.dumps(i)))

                        pagina = (raw_input("Ingrese Pagina Web Eliminar: "))
                        cadena = "http://" + str(pagina)
                        print(thing.eliminar_pagina(cadena))

                    if (op == 4):
                        print("------------------------------------------")
                        print("\t\tINFORMACION SEO PAGINA WEB\t\t")
                        # **** Contar Palabras ****
                        pagina = (raw_input("Ingrese Pagina Web: "))

                        cadena = "http://" + str(pagina)
                        longitud = len(pagina)
                        palabras = (thing.palabras(cadena))
                        a= palabras
                        print ("la cantidad de palabras de la pagina " + str(cadena) + " es :" + str(palabras))
                        palabra= str(palabras)
                        # **** Diccionario Palabras ****
                        diccionario = (thing.diccionario(cadena))
                        print ("Palabras que coinciden con el dicionario: ")
                        if (diccionario !=0):
                            for i in diccionario:
                                print(ast.literal_eval(json.dumps(i)))
                        else:
                            print ("No hay Coincidencias")
                        # **** Contar Imagenes ****
                        imagen = (thing.imagenes(cadena))
                        b= imagen
                        print("La Cantidad de Imagenes que posee la pagina " + str(pagina) + " es: " + str(imagen))
                        imagenes =str(imagen)
                        # **** Contar Enlaces Externos - Internos
                        externos = (thing.enlace_externo(cadena))
                        internos = (thing.enlace_interno(cadena))
                        c=externos
                        d=internos

                        print(
                            "La Cantidad de Enlaces Externos que posee la pagina " + str(pagina) + " es: " + str(externos))
                        print(
                            "La Cantidad de Enlaces Internos que posee la pagina " + str(pagina) + " es: " + str(internos))
                        externo = str(externos)
                        interno = str(internos)
                        # **** Analizar URL ****
                        lista = (thing.analizar_url(cadena))
                        print('\n'"\t\t\t\t\t\t\t\t******ANALISIS URL******\t\t\t\t\t\t\t\t"'\n')
                        for i in lista:
                            print(i)
                        # **** Analizar Palabras Claves(Keywords)****
                        #con_claves = -1
                        palabras_claves = (thing.analizar_keywords(cadena))
                        con_claves =0
                        print (palabras_claves)
                        if palabras_claves!= "":
                            con_claves= 1
                            e=con_claves
                        clave =str(con_claves)

                        # **** Redes Sociales****
                        redes = (thing.sociales(cadena))
                        con_redes = 0
                        for i in redes:
                            print(i)
                            con_redes += 1
                            f=con_redes
                        redes =str(con_redes)
                        # **** Enlaza Pagina Web****
                        print(thing.enlaza_pagina(cadena))
                        # **** Estructura Pagina Web ****
                        print('\n'"\t\t\t\t\t\t******ESTRUCTURA PAGINA WEB******\t\t\t\t\t\t"'\n')
                        URL = (thing.estructura_web(cadena))
                        recurso = get(URL)  # Tomar el codigo
                        pagina = BeautifulSoup(recurso.text, 'html.parser')
                        print (pagina)
                        # **** Penalizar Contenido no Apto
                        con_p = 0
                        penaliza =(thing.penalizar_pagina(cadena))
                        if penaliza !=0:
                            con_p += 1
                            g=con_p
                            for i in penaliza:
                                print(ast.literal_eval(json.dumps(i)))
                        else:
                            print ("Pagina web: " + str(cadena) + " No Penalizada (Contenido Apto) ")
                        penar =str(con_p)

                        # **** Penalizar Contenido Dudosa Reputacion ***
                        penaliza = (thing.penalizar_reputacion(cadena))
                        if penaliza != 0:
                            for i in penaliza:
                                print(ast.literal_eval(json.dumps(i)))
                        else:
                            print("Pagina web: " + str(cadena) + " No Penalizada (Contenido Buena Reputacion) ")

                        # **** Comprobar Enlaces****
                        externos = (thing.comprobar_enlaces(cadena))
                        print('\n'"\t\t\t\t\t\t******ANALISIS ENLACES EXTERNOS******\t\t\t\t\t\t"'\n')
                        for i in externos:
                            print(i)
                        suma =(a+b+c+d+e+f+g)
                        total =str(suma)

                        thing.ranking(longitud,cadena,externo,palabra,clave,interno,imagenes,penar,longitud,redes,total)

                    if (op == 5):
                        ranking = (thing.listar_ranking)
                        lista = json.loads(ranking)
                        print("**** RANKING PAGINAS WEB ****")
                        for i in lista:
                            print(ast.literal_eval(json.dumps(i)))

                        lista= ["Criterios Posicionamiento:","Imagenes","Enlaces Externos - Internos","Palabras Claves","Titulo","Palabras","Redes"]
                        for i in lista:
                            print (i)

                    if (op == 6):
                        penalizadas = (thing.listar_penalizadas)
                        lista = json.loads(penalizadas)
                        print ("**** PAGINAS PENALIZADS ****")
                        for i in lista:
                            print(ast.literal_eval(json.dumps(i)))
            else:

                verdad =True
                while verdad == True:

                    print("------------------------------------------")
                    print("\t\tMENU ADMINISTRATIVO WEB\t\t")
                    print("(1). Registro Empresas ")
                    print("(2). Agregar Palabras ")
                    print("(3). Agregra Palabras Inadecuadas")
                    print("(4). Salir")
                    op = int(raw_input("Digite una Opción: "))
                    repetir = "S"
                    if (op == 1):
                        while repetir == "S" or repetir=="s":
                            empresa = (raw_input("Ingrese Nombre Empresa: "))
                            print (thing.registro_empresas(empresa))
                            repetir =(raw_input("Desea Registrar Otra Empresa (S/N) "))

                    if (op == 2):
                        while repetir == "S" or repetir=="s":
                            palabra = (raw_input("Ingrese Palabra Clave: "))
                            print(thing.registro_empresas(palabra))
                            repetir = (raw_input("Desea Ingresar Otra Palabra (S/N) "))

                    if (op == 3):
                        while repetir == "S":
                            palabra = (raw_input("Ingrese Palabra Inadecuada: "))
                            print(thing.palabras_malas(palabra))
                            repetir = (raw_input("Desea Ingresar Otra Palabra (S/N) "))

                    if (op == 4):
                        verdad =False
                        print ("Gracias Por Utlizar Nuestros Servicios")


def main():
    marcela=Cliente()
    marcela.fernando=conexion()

if __name__ == '__main__':
    main()
