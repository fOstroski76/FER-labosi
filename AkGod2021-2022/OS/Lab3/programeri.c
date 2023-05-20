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
#include <values.h>
#include <time.h>
#include <math.h>
#include <signal.h>

int tip = 0;
int gornjaGranica = 5;
int br[2] = {0,0};
int ceka[2] = {0,0};
int posluzen[2] = {0,0};
int foodVar;
pthread_cond_t redoviUvjeta[2];
pthread_mutex_t m;


void udji_u_restoran( int tip_programera){
	
	pthread_mutex_lock(&m);
	ceka[tip_programera]++;
	
	while((br[1-tip_programera] > 0 ) || ( posluzen[tip_programera] > gornjaGranica  && ceka[1-tip_programera] > 0 )
		) { 
			
			pthread_cond_wait(&redoviUvjeta[tip_programera],&m);
			
			
		}
	
	br[tip_programera]++;
	ceka[tip_programera]--;
	posluzen[1-tip_programera] = 0;
	pthread_mutex_unlock(&m);
}


void izadji_iz_restorana( int tip_programera){
	
	pthread_mutex_lock(&m);
	br[tip_programera]--;
	posluzen[tip_programera]++;
	
	if (br[tip_programera] == 0){
		
		pthread_cond_broadcast(&redoviUvjeta[1-tip_programera]);
		//sleep(1);
		printf("Restoran je prazan.\n");
		sleep(3);
	}
	
	
	pthread_mutex_unlock(&m);
}

void* programer(void* tip_programeraVoidPtr){
	
	while(1){
		int tip_programera = *((int *)tip_programeraVoidPtr);
	 
	 
	udji_u_restoran(tip_programera);
	
	if (tip_programera == 1){
		
		printf("Linux programer je usao u restoran i sprema se jesti.\n");
				
	}
	else if (tip_programera == 0){
		
		printf("MS programer je usao u restoran i sprema se jesti.\n");
		
	}
	
	sleep(1);
	
	//sleep(1);
	
	if (tip_programera == 1){
		printf("Linux programer je izasao iz restorana.\n");
	}
	else if (tip_programera == 0){
		printf("MS programer je izasao iz restorana.\n");
	}
	//sleep(1);
	izadji_iz_restorana(tip_programera);
	sleep(0.25);
	}
}

void obradi_sigint(int sig){
	
 printf("\nUragan SIGINT razorio restoran, nece vise biti gostiju \n");
 exit(1);
 
}

int main(){
	
	// kod za maskiranje iz 1. labosa
	struct sigaction act;
	
	act.sa_handler = obradi_sigint;
	sigemptyset(&act.sa_mask);
	act.sa_flags = 0;
	sigaction(SIGINT, &act, NULL);
	
	srand(time(0));
	int brl,brm;
	int linux_tip = 1;
	int microsoft_tip = 0;
	
	pthread_cond_init(&redoviUvjeta[0], NULL);
    pthread_cond_init(&redoviUvjeta[1], NULL);
	pthread_mutex_init(&m, NULL);
	
	printf("Unesi broj Linux programera koji idu jesti:\n ");
	scanf("%d",&brl);
	
	printf("Unesi broj Microsoft programera koji idu jesti:\n ");
	scanf("%d",&brm);
	
	
	pthread_t novaTr[brl+brm]; 
	
	
	// linux = 1, MS = 0
	//while(1){
	
	for (int i = 0; i < brl; i++){
		pthread_create(&novaTr[i],NULL,&programer,&linux_tip);
	}
	
	for (size_t i = 0; i < brm; i++){
		pthread_create(&novaTr[i+brl],NULL,&programer,&microsoft_tip);
	}
	
	for (int i = 0; i < brm + brl; i++) {
    
			pthread_join(novaTr[i], NULL);
			
    }
	
	//}
	return 0;
}

