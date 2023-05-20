#include <bits/stdc++.h>

using namespace std;
  
    int brVrhova = 0;
    int brElemenata = 0;  
    int currentIndex = 0;

 int indShift(int broj){
    int counter = 1;
    while(broj >= 10){
        counter++;
        broj/=10;
    }
    return counter;

}

bool ispitajBoju(int v, bool **graf,int boja[], int b, int brVrhova) {
    
    for(int i = 0; i < brVrhova; i++)
        //Provjera je li boja b valjana za vrh v
        if (graf[v][i] && b == boja[i])
            return false;

    return true;
}

bool bojanjeGrafa(bool **graf, int m, int boja[], int v, int brVrhova) { 

    //  kad svaki vrh ima svoju boju (kraj)
    if (v == brVrhova)
        return true;

    
    for(int b = 1; b <= m; b++){

        if (ispitajBoju(v, graf, boja, b, brVrhova)) {

            boja[v] = b;

            //Rekurzivno dodjeljujemo boje ostalim vrhovima
            if (bojanjeGrafa(graf, m, boja, v + 1, brVrhova) == true)
                return true;

            //reset boju b ako ne daje dobro rj
            boja[v] = 0;
        }
    }

    //Ako se niti jedna boja ne moze dodijeliti ovome vrhu (bojanje nije moguce)
    return false;
}

int main(){
      // kod za ucitavanje iz datoteke
  string input;
    fstream inputFile("graf2.txt");

    int elementi[brElemenata];

    if(inputFile.is_open()){

    cout << endl;
    getline(inputFile,input);
    
    brVrhova = stoi(input); // n
    cout << "Broj vrhova je: " << brVrhova << endl;


    getline(inputFile,input);
    while(input.empty()) getline(inputFile,input);
    
    brElemenata = stoi(input);
    cout << "Broj elemenata je: " << brElemenata << endl;
    

    cout << "Elementi: " ;
    do{
        getline(inputFile,input); 
    }while(input.empty());
 

    //cout << input;

    for(int i = 0; i < brElemenata; i++){
        elementi[i] = stoi(input.substr(currentIndex));
        currentIndex+=(indShift(elementi[i])+1);
    }

    for(int i=0;i<brElemenata;i++){
        cout << elementi[i] <<" " ;
    }
    cout << endl;
    
    }
    
    inputFile.close();

    // kreiranje grafa pomocu matrice susjedstva
    
    bool **graf = new bool*[brVrhova];

    for (int i = 0; i < brVrhova; i++) {
        graf[i] = new bool[brVrhova];
    }

    for(int k = 0; k < brVrhova; k++) {
        for(int l = 0; l < brVrhova; l++) {
            graf[k][l] = 0;
            for(int i = 0; i < brElemenata; i++) {
                if(abs(((k+1)-(l+1)) == elementi[i])){
                    graf[k][l] = 1;
                    graf[l][k] = graf[k][l];
                }
            }
        }
    }         
    
     // komentar: max broj jedinica u nekom stupcu/retku + 1 je minimalni broj koliki ce biti krom broj (Tm 8.1.)
     
    cout << endl <<"Matrica susjedstva:" << endl;

    for(int a=0;a<brVrhova;a++){
        for(int b=0;b<brVrhova;b++){
                cout << graf[a][b] << " ";
        }
        cout << endl;
    }

    //bojanje grafa
    int boja[brVrhova];
    for (int i = 0; i < brVrhova; i++) {
        boja[i] = 0;
    }

    int kromBroj = 1;
    while(!bojanjeGrafa(graf, kromBroj, boja, 0, brVrhova)) {
        ++kromBroj;
    } 

    cout << "Kromatski broj zadanog grafa je: "<< kromBroj; 
    
    return 0;

}
  