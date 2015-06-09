#include <stdlib.h>
#include <stdio.h>
#include <math.h>
#include <assert.h>
#include <time.h>
#define DEBUG 123
#define TRUE 1
#define FALSE 0

// si elemento e pertenece al subconjunto s o no
int in(unsigned int* s, int t, int e) {
    int i = e / t; // el pedazo que contiene el elemento
    int j = e % t; // la posicion del elemento dentro del pedazo
    return ((s[i] & (1 << j)) >> j);    
}   

void add(unsigned int* s, int t, int e) { // agregar
    int i = e / t; // el pedazo que contiene el elemento
    int j = e % t; // la posicion del elemento dentro del pedazo
    s[i] |= (1 << j);
    return;       
}

void flip(unsigned int* s, int t, int e) { // cambiar 0 <-> 1
    int i = e / t; // el pedazo que contiene el elemento
    int j = e % t; // la posicion del elemento dentro del pedazo
    s[i] ^= (1 << j);
}

void del(unsigned int* s, int t, int e) {
     int i = e / t; // el pedazo que contiene el elemento
     int j = e % t; // la posicion del elemento dentro del pedazo
     if (in(s, t, e)) {
        flip(s, t, e);          
     }
     return;
}

void pick(unsigned int* s, int l, int t, int n) {
     int i, j;
     int r = (int)ceil(log(RAND_MAX)/log(2)); // bits recibidos por rand()

     for (i = 0; i < l; i++) { // para cada pedazo
         for (j = 0; j < t / r; j++) { // llenar con bits al azar
             s[i] |= rand() << r * j; // por brincos que dependen de r
         }
         if (t % r != 0) { // si no es division exacta de t entre r
            s[i] |= (rand() % (1 << (t % r))) << r * j; // llenar al tope
         }
     }
     for (i = n; i < l * t; i++) {
         del(s, t, i); // elementos no existentes entre n y l * t a cero
     }
     return;     
}

void show(unsigned int* subconjunto, int t, int n) {
  int i;
  printf("S = { ");
  for (i = 0; i < n; i++) {
      if (in(subconjunto, t, i)) {
         printf("%d ", i);
      }    
  }
  printf("}\n");
  return;     
}

double total(unsigned int* s, double* c, int t, int n) {
  int i;
  double result = 0.0;
  for (i = 0; i < n; i++) {
      if (in(s, t, i)) {
         result += c[i];
      }    
  }
  return result;     
}


int main(int algo, char** otro) {
  int i, n, l, r, elem;    
  unsigned int* subconjunto = NULL;
  double* cost = NULL;//los costos
  int t = sizeof(unsigned int) * 8; // tamanho de cada pedazo   
  // srand(time(0)); 
  #ifdef DEBUG
  n = 20; //atoi(otro[1]);
  r = 15; //atoi(otro[2]);
  #else
  n = 10000; //nuemero de clientes
  r = 1000; //numero de conjuntos
  #endif

  printf("%d elementos\n", n);
  cost = (double*)malloc(sizeof(double) * n);
  for (i = 0; i < n; i++) {
      cost[i] = 20.0 + 60.0 * (rand() / (1.0 * RAND_MAX)); // entre 20 y 80    
        #ifdef DEBUG
         printf("%d cuesta %.2f\n", i, cost[i]);
        #endif
  } 
  
  l = (int)(ceil(1.0 * n / t)); // cantidad total de pedazos requeridos
  subconjunto = (unsigned int*)malloc(sizeof(unsigned int) * l);

  pick(subconjunto, l, t, n);
  #ifdef DEBUG
         show(subconjunto, t, n);
  #endif
  for (i = 0; i < r; i++) {
        elem = rand() % n;
      if (in(subconjunto, t, elem)) { // si elem pertenece a subconjunto
         del(subconjunto, t, elem); // probar si podemos quitarlo
         assert(!in(subconjunto, t, elem)); // verificar que se haya quitado                   
      } else { // en el caso que no haya pertenecido
         flip(subconjunto, t, elem); // cambiamos ese bit
         assert(in(subconjunto, t, elem)); // ahora deberia pertenecer                   
      }
      #ifndef DEBUG
      if (r % 100 == 0) {
            #endif
      printf("%.2f\n", total(subconjunto, cost, t, n));
      #ifndef DEBUG
      }
      #endif

  #ifdef DEBUG
   printf("Modificando a la pos. %d\n", elem);
   show(subconjunto, t, n);
  #endif

  }
  free(subconjunto);
  free(cost);
  printf("todo bien\n");
  getchar();  
 return 0;   
}
