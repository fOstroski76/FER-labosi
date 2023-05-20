#include <iostream>
#include <math.h>

using namespace std;

// Fran Ostroški 

// Rjesenja karakteristicne kvadratne jdzbe

  long double nulToc1 (long double a, long double b, long double c){
   long double rez = (-b + sqrt(b*b-4*a*c) )/ (2*a) ;

   return rez ;
  }
 
 long double nulToc2 (long double a, long double b, long double c){

   long double rez = (-b - sqrt(b*b-4*a*c) )/ (2*a) ;

   return rez;
  }

 
 //fja za opce homogeno rj
  void opcaFormula(long double lambda1, long double lambda2, long double a_0, long double a_1, int n){
    
   long double nultocka1 = nulToc1(1,-lambda1,-lambda2); // a je uvijek = 1!
   long double nultocka2 = nulToc2(1,-lambda1,-lambda2); // minusi zbog prebacivanja na drugu stranu!
   long double rjesenje = 0, koef_1 = 0,koef_2 = 0;
  
   if(nultocka1 == nultocka2) {
      
      koef_1 = a_0;
      koef_2 = (a_1-koef_1*nultocka1)/nultocka1;  // rjesenja sustava
      
      rjesenje = koef_1*pow(nultocka1,n) + koef_2*n*pow(nultocka2,n);
      cout << rjesenje;
   }
    else {
     
     koef_1 = (a_1 - a_0*nultocka2)/(nultocka1 - nultocka2);
     koef_2 = a_0 - koef_1; // rjesenja sustava

     rjesenje = koef_1*pow(nultocka1,n) + koef_2*pow(nultocka2,n);
     cout << rjesenje;
     
    }

  }

 //rekurzivna fja 
  long double rekurzivniNacin (long double lambda1, long double lambda2, long double a_0, long double a_1, int n){

     if (n == 0) return a_0;
     if (n == 1) return a_1;

     return lambda1*rekurzivniNacin(lambda1,lambda2,a_0,a_1,n-1) + lambda2*rekurzivniNacin(lambda1,lambda2,a_0,a_1,n-2);

  }


int main(void){

    long double lambda1, lambda2, a_0, a_1;
    int n;
    

  cout << "Unesite prvi koeficijent λ_1 rekurzivne relacije: " ;
   cin >> lambda1; 
  cout << endl; 

  cout << "Unesite drugi koeficijent λ_2 rekurzivne relacije: " ;
   cin >> lambda2;
  cout << endl;

  cout << "Unesite vrijednost nultog clana niza a_0: " ;
   cin >> a_0;
  cout << endl;

  cout << "Unesite vrijednost prvog clana niza a_1: " ;
   cin >> a_1;
  cout << endl;

  cout << "Unesite redni broj n trazenog clana niza: " ;
   cin >> n;
  cout << endl;

  // fja za opce homogeno rj
  cout << "Vrijednost n-tog clana niza pomocu formule: ";
  opcaFormula(lambda1,lambda2,a_0,a_1,n);
  cout << endl;

  //rekurzivna fja 
  cout << "Vrijednost n-tog clana niza iz rekurzije: " << rekurzivniNacin(lambda1,lambda2,a_0,a_1,n);
  cout << endl;
  
   return 0;
}

