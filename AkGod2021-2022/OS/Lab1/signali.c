#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <signal.h>
#include <math.h>


/* funkcije za obradu signala, navedene ispod main-a */

void obradi_dogadjaj(int sig);
void obradi_sigterm(int sig);
void obradi_sigint(int sig);

int nije_kraj = 1;

 // globalna varijabla i imena datoteka
 
	int mainNumber;
	FILE *status;
	FILE *obrada;

int main(){
	
	 // kopirano iz uputa za vjezbu
	 
	struct sigaction act;
/* 1. maskiranje signala SIGUSR1 */
	act.sa_handler = obradi_dogadjaj; /* kojom se funkcijom signal obrađuje */
	sigemptyset(&act.sa_mask);
	sigaddset(&act.sa_mask, SIGTERM); /* blokirati i SIGTERM za vrijeme obrade */
	act.sa_flags = 0; /* naprednije mogućnosti preskočene */
	sigaction(SIGUSR1, &act, NULL); /* maskiranje signala preko sučelja OS-a */
 
 /* 2. maskiranje signala SIGTERM */
	act.sa_handler = obradi_sigterm;
	sigemptyset(&act.sa_mask);
	sigaction(SIGTERM, &act, NULL);
 
 /* 3. maskiranje signala SIGINT */
	act.sa_handler = obradi_sigint;
	sigaction(SIGINT, &act, NULL);
	
	printf("Program s PID=%ld krenuo s radom\n", (long) getpid());
 /* neki posao koji program radi; ovdje samo simulacija */
	
	// kraj kopiranog dijela 
	
	
	status = fopen("status.txt","r");
	fscanf(status,"%d",&mainNumber);  // procitaj broj iz status.txt
	fclose(status);
	
	 //  citaj brojeve iz obrada.txt dok ne dodje do kraja datoteke, mijenjaj number
	if (mainNumber == 0) {
		
		obrada = fopen("obrada.txt","r");
		int idiKrozFile;
		fscanf(obrada,"%d",&idiKrozFile);
				
		while(!feof(obrada)){
			
			fscanf(obrada,"%d",&idiKrozFile);
						
		}
		
		mainNumber = sqrt(idiKrozFile);  
		fclose(obrada);
	}
	
	// upis nule u status.txt
	 
	status = fopen("status.txt","w");
	fprintf(status,"%d",0);
	fclose(status);
	
	// beskonacna petlja
	
	while(nije_kraj) {
		
		mainNumber+=1;
		int x;
		x = pow(mainNumber,2);
		
		obrada=fopen("obrada.txt","a");
		fprintf(obrada,"%d",x);
		fprintf(obrada,"\n");
		fclose(obrada);
		
	printf("Program: iteracija %d\n", mainNumber);
	sleep(5);
	
	}
	
	printf("Program s PID=%ld zavrsio s radom\n", (long) getpid());
	

	return 0;
}

void obradi_dogadjaj(int sig){
	
	printf("Trenutni broj: %d\n",mainNumber);
	
}

void obradi_sigterm(int sig){
	
	status = fopen("status.txt","w");
	fprintf(status,"%d",mainNumber);
	fclose(status);
	
	printf("Primio signal SIGTERM, pospremam prije izlaska iz programa\n");
	nije_kraj = 0;
	
}


void obradi_sigint(int sig){
	
 printf("Primio signal SIGINT, prekidam rad\n");
 exit(1);
 
}


