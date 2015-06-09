##Este es el generador del archivo batch para generar y ejecutar las instancias.
##Al ejecutar cambiar directorio de la ubicacion de los archivos

archivo = open("C:\\Users\\DELL\\Desktop\\heuristico\\Resultados\\generar.bat",'w')

clientes =  600
CD = 55
plantas= 35
repeticiones = clientes * 5

for r in xrange(1,5):
        for c in xrange(100,clientes,50):
                for cd in xrange(20,CD,5):
                        for p in xrange(10,plantas,5):
                                print>>archivo, 'python columnas.py  %d    %d    %d    %d     %d'%(p,cd,c,r,c*50);
                                                                
archivo.close()
