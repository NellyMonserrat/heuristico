# -*- coding: utf-8 -*-

from random import randint
from math import ceil,sqrt
from sys import argv
from time import clock
t0 = clock()

##Se ingresa la cardinalidad de los conjuntos (Plantas, Clientes  y Centros)
Plantas = int(argv[1]) 
Centros = int(argv[2])
Clientes = int(argv[3])
replica = int (argv[4]) ##El número de repeticiones para la instancia
deseados = int (argv[5]) ##Núm de subconjuntos deseados
intentos = Plantas * Centros * deseados ##Máximo de intentos para la creacion de los subconjuntos

##Listas para almacenar las clases de cada conjunto
CDs, Plants= [],[]
Retailers, Asignacion = [] ,[]

##Parámetros del problema
aux = 0
h = 0.5
lamda = 360
tetha, beta = 1,1
za, zg = 0.67, -0.8416
ze = za - zg
captotal, demtotal= 0, 0
maximo, prototal = 0, 0
tau = sqrt(2*lamda/(tetha*h))
bas= tetha * h *lamda * za
Bp = beta * lamda
n= sqrt (2 * tetha * h *lamda)
Demanda, Varianza = {}, {}

class cliente:
    def __init__(self, nombre):
                    self.nombre = nombre
                    self.demanda = randint (5,60)
                    self.varianza = randint (5,95)
class CD:
    def __init__(self,nombre):
            self.nombre = nombre
            self.capCD = randint (maximo*20, demtotal*20)
            self.ctol = ceil (0.45 * self.capCD)
            self.ctoo = randint (40,150)
            self.ctot = list ()
            for retail in xrange (Clientes):
                    self.ctot.append(randint(1,7))

class plantas:
    def __init__(self,name):
            self.name =name
            self.produccion = randint (5*demtotal/(2*Plantas),demtotal)
            self.g = list ()
            self.a = list ()
            self.l = list ()
            for c in xrange (Centros):
                    self.g.append(randint(25,70))
                    self.a.append(randint(2,12))
                    self.l.append(randint(1,8))
                            
for k in xrange(Clientes):
    Retailers.append(cliente(k))
    demtotal = demtotal + Retailers[k].demanda
    if (maximo < Retailers[k].demanda):
            maximo = Retailers[k].demanda
    
for j in xrange(Centros):
    CDs.append(CD(j))
    captotal += CDs[j].capCD
    
##Asegurar capacidad para atender la demanda
while captotal < (demtotal * 20 * Centros):
    for candidatos in CDs:
            captotal += candidatos.capCD*5
            candidatos.capCD *= 6

##Asegurar capacidad de producción para atender demanda
for i in xrange (Plantas):
    i = plantas(i)
    Plants.append(i)
    prototal += i.produccion
while prototal < demtotal *5:
    for i in xrange(Plantas):
            prototal =Plants[i].produccion
            Plants[i].produccion = Plants[i].produccion *2  

##Diccionario con datos de los subconjuntos, integrantes y costos
subconjuntos = dict ()

##Auxiliares
intento, deseado = 0, 0
repeticion = True

while intento < intentos and  deseado < deseados+1:
    agregacion = [1,Centros]
    if intento > 1:
            try:
                Sub = randint (2,Centro-1)
            except:
                Sub = 2
    else:
            Sub = agregacion[intento]
            if intento == 1:
                repeticion = False
    for j in xrange(Centros):
        Demanda[j] = 0
        Varianza[j] = 0
        subconjuntos [j] =[]
    for j in xrange(Clientes):
        seleccion = randint(0, Sub-1) ## a cada cliente se le asigna un subconjunto
        if Sub == 1 or Sub == Centros:
            repeticion = True
        subconjuntos[seleccion].append(j) ##se colocan los clientes dependiendo en que CD son asignados
        Demanda[seleccion] += Retailers[j].demanda ## a ese subconjunto se guarda la demanda del cliente
        Varianza[seleccion] += Retailers[j].varianza


    for s in xrange(Centros): ##Por cada CD seleecionado ...
        factible = True
        if Demanda[s] > 0:
            for i in xrange (Plantas):
                for j in xrange(Centros):
                    P1 = sqrt (Demanda[s]* (CDs [j].ctoo + beta * Plants [i].g[j]))
                    P2 = sqrt(Varianza[s] * Plants[i].l[j])
                    ocupacion = ceil(tau * P1 + ze * P2 )
                    if ocupacion <= CDs[j].capCD:
                        Asignacion.append([subconjuntos[s],i,j,P1*bas + n*P2])
                        ##print Asignacion [-1]
                    else:
                        factible = False
        if factible == True:
            deseado += 1
                            
    subconjuntos.clear() ##Limpiar diccionario para la creación de nuevas columnas 
    intento += 1

final=(clock ()-t0) * 1000 ##Calcular el tiempo que tomo la creación de lso conjuntos
salida = open ('resultados.dat','a')
salida.write('%d*%d*%d*%d*%d*%0.2f\n'%(replica,Plantas,Centros,Clientes,deseados,final))
salida.close()
