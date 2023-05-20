#include <stdio.h>
#include <sys/types.h>
#include <sys/ipc.h>
#include <sys/shm.h>
#include <sys/sem.h>
#include <sys/msg.h>
#include <values.h>
#include <signal.h>
#include <stdlib.h>
#include <unistd.h>
#include <time.h>
#include <math.h>
#include <sys/wait.h>
#include <sys/types.h>
#include <pthread.h>

// inacica laboratorijske vjezbe za neparni jmbag!!


	void obradi_sigint(int sig);
	
// globalne konstante

	FILE *output;
	int id;
	int *globalnaVar,globalnaVar2;

// fja za posao radne dretve
void posaoradnedretve(int brojRandomProlaza){
	
	for (int i = 0; i < brojRandomProlaza; i++){
			
			while (*globalnaVar == 0){
               // printf("Cekam...\n")
			}
			
        int uvecanBroj = *globalnaVar;
        printf("RADNA DRETVA: pročitan broj %d i povećan na %d\n", uvecanBroj, uvecanBroj+1);
		globalnaVar2 = ++ *globalnaVar;
        usleep(70);  //sleep(1); (sporija varijanta)
        *globalnaVar = 0;
		}
}

// fja za izlazni proces a.k.a. novostvorenu dretvu u dijetetu
void *ispisdretve(void *brrnd){
	output = fopen("output.txt","a");
	 int *brojRandomProlaza = brrnd;
	for (int i = 0; i < *brojRandomProlaza; i++){
			
		while (globalnaVar2 == 0){
               // printf("Cekam...\n")
		}
		
		usleep(20); // sleep(1); (sporija varijanta)
		fprintf(output, "%d\n", globalnaVar2);
		printf("IZLAZNI PROCES: broj upisan u datoteku %d\n", globalnaVar2);
		printf("\n");
		globalnaVar2 = 0;		
	}
	fclose(output);
}

void ocisti(){   // kod iz uputa
		/* oslobađanje zajedničke memorije */ 
   (void) shmdt((char *) globalnaVar);
   (void) shmctl(id, IPC_RMID, NULL);
   
   exit(0);
    
	}

void obradi_sigint(int sig){
	
 printf("Primio signal SIGINT,pokrecem ciscenje memorije i prekidam rad!\n");
 ocisti();
 exit(1);
 
}

int main(void){
	
	// maskiranje siginta, iz vjezbe 1	

	struct sigaction act;
	
	act.sa_handler = obradi_sigint;
	sigemptyset(&act.sa_mask);
	act.sa_flags = 0;
	sigaction(SIGINT, &act, NULL);
	
	
	   // kod iz uputa 
	 /* zauzimanje zajedničke memorije */
   id = shmget(IPC_PRIVATE, sizeof(int), 0600);
 
   if (id == -1)
      exit(1);  /* greška - nema zajedničke memorije */
  
   globalnaVar = (int *) shmat(id, NULL, 0);
   *globalnaVar = 0;
   sigaction(SIGINT,&act,NULL);//u slučaju prekida briši memoriju
   
   int brojRandomProlaza;
   scanf("%d",&brojRandomProlaza);
    
   
   printf("Pokrenuta RADNA DRETVA\n");
   // stvaranje novog procesa    
	int pid = fork();
	if(pid == 0){
		
		// kreiranje i cekanje kraja za izlaznu dretvu
		printf("Pokrenut IZLAZNI PROCES\n\n");
		
		pthread_t noviTr;
		pthread_create(&noviTr, NULL, &ispisdretve, &brojRandomProlaza);
		posaoradnedretve(brojRandomProlaza);
		pthread_join(noviTr, NULL);
		exit(0);
		
	}
	else if(pid == -1){
		printf("greska");
	}
	// rad ulazne dretve 
	
	printf("Pokrenuta ULAZNA DRETVA\n");
	srand(time(0));
   for(int i = 0; i < brojRandomProlaza; i++) {
	   
	   int randomBrojSekundi,randomBroj;
	   
	   randomBrojSekundi = rand()%5 + 1; // DG = 1 , Interval = 5
	   sleep(randomBrojSekundi);
	   
	   randomBroj = rand()%100 +1; // DG = 1, Interval = 100
	   printf("ULAZNA DRETVA : broj %d\n ",randomBroj);
	   *globalnaVar = randomBroj;
   }
	waitpid(pid, NULL, 0);
	
	ocisti(0); // ukloni sve potencijalne viskove u memoriji
	
	return 0;
}

















