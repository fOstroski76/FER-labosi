#include <bits/stdc++.h>

using namespace std;

   int tezinaBrida(int k, int l, int a, int b){
       int rezultat = 0;
       rezultat = (a*k+b*l)*(a*k+b*l)+1;
       return rezultat;
   }

    

int main(void){

    int n,a,b;
    cout << "Unesite redom, odvojene razmakom, parametre n,a i b: " ;
    cin >> n >> a >> b;
    int matrica [n][n];

    // kreiranje tezinske matrice susjedstva 
    cout << endl << "Tezinska matrica susjedstva: " << endl;
    for(int i=0;i<n;i++){
        for(int j=0;j<n;j++){
            if(i<j) {
                matrica[i][j] = tezinaBrida(i+1,j+1,a,b);
                matrica[j][i] = matrica[i][j];

            }
            if(i==j) {
                matrica[i][j] = 0;
                matrica[j][i] = matrica[i][j];

            }
        }
    }

    for(int i=0;i<n;i++){
        for(int j=0;j<n;j++){
            cout << " " << setw(6) << matrica[i][j] << " ";
        } 
        cout << endl;
    }
    
    cout << endl;

    // iscrpna pretraga

    int vrhovi[n];
    for(int i=0;i<n;i++){
        vrhovi[i] = i+1;
    }

     int minIscrpni = INT_MAX;
     do{
        int sum = 0;
        int i;
        for(i=0;i<n-1;i++){
            sum+=matrica[(vrhovi[i]-1)][(vrhovi[i+1]-1)];
         //   cout << sum << " ";
        }
        sum+=matrica[(vrhovi[i]-1)][(vrhovi[0]-1)];
          //  cout << sum << " ";
        if(sum < minIscrpni) minIscrpni = sum;
        //cout << min <<" ";
    }while(next_permutation(vrhovi+1,vrhovi+n));

    cout << endl << "Iscrpni algoritam nalazi ciklus duljine " << minIscrpni << endl;
 

    // pohlepni algoritam

  cout << endl;
  int k,l;
  int najmanjiBrid = tezinaBrida(1,2,a,b), minVrhK = 1, minVrhL = 2; // minimum je kad su l,k = (1,2) ili (2,1) ,po formuli
  int tezina;
 
 for(int i=0;i<n;i++){    // trazenje najmanjeg brida ( just in case provjera)
        for(int j=0;j<n;j++){
            if(matrica[i][j] < najmanjiBrid  && matrica[i][j] != 0) {
            najmanjiBrid = matrica[i][j];
            minVrhK = i+1;
            minVrhL = j+1;

            }
        }
    } 
  
  //  cout << "Najmanji brid:" << najmanjiBrid;

  int suma = najmanjiBrid;
  bool nijePredjeni[n + 1];

  for (int i = 1; i <= n; i++) {
    nijePredjeni[i] = true;
  }

  k = minVrhK;
  l = minVrhL;
  nijePredjeni[k] = false;
  nijePredjeni[l] = false;

  int k2, l2;

  for (int i = 0; i < n-2; i++) {
    najmanjiBrid = -1;
    for (int j = 1; j <= n; j++) {
      if (nijePredjeni[j] == true) {
        k2 = min(k, j);
        l2 = max(k, j);
        tezina = tezinaBrida(k2,l2,a,b);
        if (najmanjiBrid == -1 || tezina < najmanjiBrid) {
          najmanjiBrid = tezina;
          minVrhK = min(j, l);
          minVrhL = max(j, l);
        }
        k2 = min(l, j);
        l2 = max(l, j);
        tezina = tezinaBrida(k2,l2,a,b);
        if (najmanjiBrid == -1 || tezina < najmanjiBrid) {
          najmanjiBrid = tezina;
          minVrhK = min(k, j);
          minVrhL = max(k, j);
        }
      }
    }

    suma+=najmanjiBrid;
    nijePredjeni[minVrhK] = false;
    nijePredjeni[minVrhL] = false;
    k = minVrhK;
    l = minVrhL;
  }
  k2 = min(k, l);       // dodavanje zadnjeg brida (onog koji dira pocetni)
  l2 = max(k, l);
  suma+=tezinaBrida(k2,l2,a,b);

  cout << "Pohlepni algoritam nalazi ciklus duljine " << suma << endl;

  if(suma == minIscrpni) cout << endl << "Pohlepni algoritam daje optimalno rjesenje!" << endl;
  else cout << endl << "Pohlepni algoritam ne daje optimalno rjesenje!" << endl;
    
    return 0;
}