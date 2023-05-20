#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
#include <unistd.h>
#include <string.h>
#include <sys/types.h>
#include <sys/ipc.h>
#include <sys/shm.h>
#include <sys/sem.h>
#include <sys/msg.h>
#include <sys/wait.h>
#include <values.h>
#include <time.h>
#include <math.h>
#include <signal.h>
#include <semaphore.h>

#define BR_MJESTA_VRTULJKA 5


int memId;                                 // inicijalizacija varijabli
sem_t *prvi, *drugi,*treci,*cetvrti;

void vrtuljak(){
	
	while(1){
		
		printf("Vrtuljak čeka na posjetitelje!\n");
		for (int i = 0; i < BR_MJESTA_VRTULJKA; i++){
			sem_post(prvi); 
		}
		
		
		
		for(int i = 0; i < BR_MJESTA_VRTULJKA; i++){ 
            sem_wait(drugi);
        }
		printf("Pokrećem vrtuljak!\n\n");
		for(int i = 0; i < 3; i++){
			printf("Voznja u tijeku....\n");
			sleep(0.5);
		}
		printf("\nZaustavljam vrtuljak!\n\n");
		
		for(int i = 0; i < BR_MJESTA_VRTULJKA; i++) { 
            sem_post(treci);
        }

        for(int i = 0; i < BR_MJESTA_VRTULJKA; i++){
            sem_wait(cetvrti);
        }
        
		printf("\n\n\n");
        sleep(3);
	}
	
}

void posjetitelj(int brPosjetitelja){
	
	while(1){
	sem_wait(prvi);
    printf("Posjetitelj %d ušao i sjeo u vrtuljak.\n",brPosjetitelja+1);
    sem_post(drugi);
    sem_wait(treci);
     printf("Posjetitelj %d se digao i izašao iz vrtuljka (i nadamo se uzivao).\n",brPosjetitelja+1);
    sem_post(cetvrti);
	}
}
void ocisti(){  // za oslobadjanje memorije 
    sem_destroy(prvi);
    sem_destroy(drugi);
    sem_destroy(treci);
    sem_destroy(cetvrti);

    (void) shmdt((sem_t *)prvi);
    (void) shmdt((sem_t *)drugi);
    (void) shmdt((sem_t *)treci);
    (void) shmdt((sem_t *)cetvrti);

    (void) shmctl(memId, IPC_RMID, NULL);
}

void obradi_sigint(int sig) {
    printf("\nOgromni gorila SIGINT skocio je na vrtuljak i otjerao putnika!\n");
	ocisti();
	exit(0);
}
int main () {
	
	sleep(3);    // kod za maskiranje iz 1. labosa
	struct sigaction sig;

	sig.sa_handler = obradi_sigint;
    sigemptyset(&sig.sa_mask);
    sig.sa_flags = 0;
	sigaction(SIGINT, &sig, NULL);
	
	
	memId = shmget(IPC_PRIVATE,4*sizeof(sem_t),0600);
	if (memId == -1){
		exit(1);
	}
	sem_t *ptr = (sem_t*) shmat(memId,NULL,0);
	prvi = ptr; // vrtuljak je prazan
	drugi = ptr + 1; // putnici sjeli
	treci = ptr + 2; // putnici smiju napustiti vrtuljak
	cetvrti = ptr+ 3; // putnici izasli
	
	int prviInit,drugiInit,treciInit,cetvrtiInit;
	
	prviInit = sem_init(prvi,1,0);
	if (prviInit == -1){
		exit(1);
	} 
	drugiInit = sem_init(drugi,1,0);
	if (drugiInit == -1){
		exit(1);
	}
	treciInit = sem_init(treci,1,0);
	if (treciInit == -1){
		exit(1);
	}
	cetvrtiInit = sem_init(cetvrti,1,0);
	if (cetvrtiInit == -1){
		exit(1);
	}
	
	if(fork() == 0){
		printf("Brzinski gradim lunapark i ringišpil...\n");
		vrtuljak();
	}
	int pid;
	for(int i=0; i < BR_MJESTA_VRTULJKA; i++){
		if( pid = fork() != 0){
			posjetitelj(i);
			exit(0);
			waitpid(pid, NULL, 0);
		}
	}
	
	return 0;
}