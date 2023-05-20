#include <stdio.h>
#include <math.h>
#include <string.h>
#include <signal.h>
#include <stdlib.h>
#include <time.h>
#include <unistd.h>
#include <stdbool.h>
#define TMAX 32

    int m; // broj okvira
    int n; // broj procesa
    

void obradi_sigint(int sig) {

    printf("\nZavrsavam s radom!\n");
	exit(0);
}

int dekUBin(int broj){

    if(broj < 2){
        return broj;
    }
    else {
        return dekUBin(broj / 2) * 10 + broj % 2;
    }

}

int main(){


    struct sigaction sig;

	sig.sa_handler = obradi_sigint;
    sigemptyset(&sig.sa_mask);
    sig.sa_flags = 0;
	sigaction(SIGINT, &sig, NULL);

    srand(time(0));
    printf("Unesite broj okvira (m) i broj procesa(n)");
    scanf("%d %d",&m,&n);
    
    printf("m:%d ",m);
    printf("n:%d\n",n);

    int disk[n][16]; // max 16 str jer koristimo 4b adresiranje
    int okvir[m];
    short tablicaStr[n][16];

    // incijalizacija svega na 0 

    for(int i = 0; i< n;i++){
        for(int j = 0; j < 16; j++){
            disk[i][j] = 0;
            tablicaStr[i][j] = 0;
        }
    }

    for(int i=0; i< m; i++){
        okvir[m] = 0;
    }
    // 

    int t = 0;
    int randBr,randBrBin,sadrzaj,noviOkvir;
    int adrBitovi = 0,pronadjenOkvir = 0;
    int tempOdbacenOkvir[m];

    while(1){

        for(int i = 0; i < n; i++){

            randBr = (rand() % 1024) & 0x3FE; // 0x1FE
            randBrBin = dekUBin(randBr);

            // randBr : xxxxxx|xxxx|xxxxxx
            //      prazno  adr. bitovi  pomak

            for(int j = 0; j < 3; j++){
                 printf("\n");
            }
           
            printf("\n Proces : %d, t : %d\n",i,t);
            printf("\tLogicka adresa (hex) : 0x%04x, bin: %d\n",randBr,randBrBin);  

            adrBitovi = randBr / 0b1000000 ;  //  /(2^6) 
            // print("%d\n",adrBitovi);

            if(!(tablicaStr[i][adrBitovi] & (short)0b100000)){

                printf("\tPromasaj!\n");

                int indexStr[m]; 
                for(int i = 0; i < m; i++){

                    indexStr[i] = 0;
                }

                for(int i = 0; i < m; i++){

                    tempOdbacenOkvir[i] = 0;
                    indexStr[i] = -1;

                }

                pronadjenOkvir = 0;

                for(int i = 0; i < n; i++){
                    for(int j = 0; j < 16; j++){

                        int podatci = tablicaStr[i][j];

                        //  tablica: xxxxxxxxxx|x|xxxxx
                        //           fiz. adr   pris   LRU 

                        bool jePrisutan = (podatci & 0b100000);

                        if(jePrisutan == true){

                            noviOkvir = podatci / 0b1000000;
                			tempOdbacenOkvir[noviOkvir] = podatci;
                			indexStr[noviOkvir] = 1;

                        }
                        
                    }
                }

                int tMin = 32,minOkvir = 0,minStr = 0; 

                for(int i = 0; i < m; i++) {
					if(tempOdbacenOkvir[i] == 0) {

						pronadjenOkvir = i;
						break;

					} else {

						if((tempOdbacenOkvir[i] & 0b11111) < tMin) {

							tMin = tempOdbacenOkvir[i] & 0b11111;
							minOkvir = i;
							minStr = indexStr[i];

						}
					}
				}

                int noviPodatci = 0;

                if(pronadjenOkvir >= 0) {

					printf("\t\tDodijeljen okvir 0x%04x\n", pronadjenOkvir);

					noviPodatci = (((pronadjenOkvir * 0b1000000) | 0b100000) | t);
					okvir[pronadjenOkvir] = disk[i][adrBitovi];
					tablicaStr[i][adrBitovi] = noviPodatci;

				} else {

                    for(int i = 0; i < n; i++){

                        bool jePrisutan2 = tablicaStr[i][minStr];

                        if((jePrisutan2 == true) && ((tablicaStr[i][minStr] / 0b1000000) == minOkvir)){

                            tablicaStr[i][minStr] = 0;
                            disk[i][minStr] = okvir[minOkvir];

                            printf("\t\tIzbacujem stranicu 0x%04x iz procesa %d\n", minStr * 0b1000000, i);
							printf("\t\tLRU izbacene stranice: 0x%04x\n", tMin);
							printf("\t\tDodijeljen okvir 0x%04x\n", minOkvir);

							break;
                        }

                    }

                    noviPodatci = (((pronadjenOkvir * 0b1000000) | 0b100000) | t);
					okvir[minOkvir] = disk[i][adrBitovi];
					tablicaStr[i][adrBitovi] = noviPodatci;

                }
                tablicaStr[i][adrBitovi] = noviPodatci;

            }
            
            int fizAdr = ((tablicaStr[i][adrBitovi] & 0b1111111111000000) | (randBr & 0b111111));
            printf("\tFiz. adresa: 0x%04x\n",fizAdr); 

            int tablZapis = (tablicaStr[i][adrBitovi] & 0b111111);
			printf("\tZapis u tablici: 0x%04x\n",tablZapis);

            int podatciAdr = okvir[tablicaStr[i][adrBitovi] / 0b1000000];
			printf("\tPodatci na adresi: %d\n",podatciAdr);
			
            for (int i = 0; i < 2; i++){
                printf("\n");
            }

            t++;

            if(t == TMAX) {
				for(int i = 0; i < n; i++) {
                    for(int j = 0; j < 16; j++) {
                        tablicaStr[i][j] = tablicaStr[i][j] & 0b1111111111100000;
                    }
                }

                tablicaStr[i][adrBitovi] = tablicaStr[i][adrBitovi] | 0b1;
                t = 0;
			}

            sleep(2);
        }
        
        
    }

    return 0;



}