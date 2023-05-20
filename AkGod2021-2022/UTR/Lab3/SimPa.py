
import string
from sys import stdin
import sys
                       
# 1. redak
ulazniNizovi = sys.stdin.readline().strip().split("|")
#print(ulazniNizovi)

#2. redak
skupSt = sys.stdin.readline().strip().split(",")
#print(skupSt)

#3. redak
skupUlZn = sys.stdin.readline().strip().split(",")
#print(skupUlZn)

#4. redak
skupZnStog = sys.stdin.readline().strip().split(",")
#print(skupZnStog)

# 5. redak 
skupPrihvStanja = sys.stdin.readline().strip().split(",")
#print(skupPrihvStanja)

# 6. redak
pocStanje = sys.stdin.readline().strip()
#print(pocStanje)

# 7. redak
pocZnStog = sys.stdin.readline().strip()
#print(pocZnStog)

#8. redak nadalje 
dictPrijelaza = dict()

for line in sys.stdin:
    prijelaz = line.strip()
    #print(prijelaz)
    temp = prijelaz.split("->")
    lijevaStr = temp[0]
    desnaStr = temp[1]

    novoStanje = desnaStr.split(",")[0]
    noviNizStoga = desnaStr.split(",")[1]
    #print(novoStanje + " " + noviNizStoga)

    temp2 = lijevaStr.split(",")
    #print("temp2 :",temp2)
    trenutnoStanje = temp2[0]
    ulazniZnak = temp2[1]
    znakStoga = temp2[2]
    tuplePrijelaza = (trenutnoStanje,znakStoga)
    #print(tuplePrijelaza)
    tupleNovogStanja =(novoStanje,noviNizStoga)
    #print(tupleNovogStanja)
    dictPromjene = dict()

    if tuplePrijelaza in dictPrijelaza.keys() :
        dictPromjene = dictPrijelaza[tuplePrijelaza]
    dictPromjene[ulazniZnak] = tupleNovogStanja
    dictPrijelaza[tuplePrijelaza] = dictPromjene

#print(dictPrijelaza)

# simulacija 


for ulazniNiz in ulazniNizovi :
    stog = []
    stog.append(pocZnStog)
    ispis = ""
    ispis += (pocStanje + "#" + pocZnStog + "|")
    #print(stog)
    #print(ispis) 
    trenSt = pocStanje
    trenZnStog = pocZnStog
    trenutniTuple =(trenSt,trenZnStog)
    
    brOcitanihSimbola = 0
    br = False
    ulazniSimboli = ulazniNiz.split(",")
    if br == False :
        ulazniSimboliPocetni = ulazniSimboli.copy()
        br = True
    procitaniSimboli = list()
    for ulSimb in ulazniSimboli :
        brOcitanihSimbola += 1
        if brOcitanihSimbola == len(ulazniSimboli)  :
           ulazniSimboli.insert(brOcitanihSimbola+1,"$")
           
        tempVarSimb = ulSimb
        trenutniTuple =(trenSt,trenZnStog) 
        drugiTrenutniTuple = trenutniTuple
        #print(ulazniSimboli)
       
                
        #print("Trenutni tuple je:",trenutniTuple)
        if trenutniTuple[1] != "$" and trenutniTuple in dictPrijelaza.keys()  :
            #print(dictPrijelaza[trenutniTuple],trenutniTuple)
            if ulSimb in dictPrijelaza[trenutniTuple].keys() and "$" not in dictPrijelaza[trenutniTuple].keys()  :
                
                #print(ulSimb," ,trenutni tuple:",trenutniTuple,"  ,trenutni stog:" ,stog)
                nemaPonavljanja=0
                for key in dictPrijelaza.keys() :
                    for key2 in dictPrijelaza[trenutniTuple].keys() :

                        if key[0] == trenutniTuple[0] and key[1].startswith(trenZnStog) and nemaPonavljanja < 1 and key2 == ulSimb:
                            nemaPonavljanja += 1
                        
                            #print("Ovaj trenutni tuple ide u:",dictPrijelaza[trenutniTuple][ulSimb])
                        
                            if len(dictPrijelaza[trenutniTuple][ulSimb][1]) != 1 :
                                #stog[-1] = stog[-1][0]
                            
                                stog.append(dictPrijelaza[trenutniTuple][ulSimb][1] + stog[-1][1:])
                            

                            elif len(dictPrijelaza[trenutniTuple][ulSimb][1]) == 1 : 
                                if len(stog[-1]) == 1 :
                                    stog.append(dictPrijelaza[trenutniTuple][ulSimb][1])
                                else :
                                    stog.append(dictPrijelaza[trenutniTuple][ulSimb][1] + stog[-1][1:])
                            

                            if dictPrijelaza[trenutniTuple][ulSimb][1] != "$" :
                                ispis += (dictPrijelaza[trenutniTuple][ulSimb][0] + "#" +stog[-1] + "|" )
                                #print("dodatak ispisu",ispis,brOcitanihSimbola,len(ulazniSimboliPocetni))

                            trenSt =  dictPrijelaza[trenutniTuple][ulSimb][0]
                            trenZnStog = stog[-1][0]
                            #print("TrenZnStog:",trenZnStog)
                        
                            if trenZnStog == "$" :
                                stog.append(stog[-2][1:])
                                
                                if(bool(stog[-1]) == True) :
                                    trenZnStog = stog[-1][0]
                                    ispis += (dictPrijelaza[trenutniTuple][ulSimb][0] + "#" +stog[-1] + "|" )
                                    #print("dodatak ispisu",brOcitanihSimbola,len(ulazniSimboliPocetni))
                        
                                else :
                                    stog.append("$")
                                    trenZnStog = stog[-1][0]
                                    ispis += (dictPrijelaza[trenutniTuple][ulSimb][0] + "#" +stog[-1] + "|" )
                                    #print("dodatak ispisu",brOcitanihSimbola,len(ulazniSimboliPocetni))
                            #print(ispis)
                            #print("Novo trenutno(poc) stanje bude:",trenSt, ", novi TrenZnStog je: ",trenZnStog)
                           

                
            elif "$" in dictPrijelaza[trenutniTuple].keys()  :
                #print(ulSimb," ,trenutni tuple:",trenutniTuple,"  ,trenutni stog:" ,stog)
                nemaPonavljanja=0
                #print("Tu")
                for key in dictPrijelaza.keys() :
                    for key2 in dictPrijelaza[trenutniTuple].keys() :
                        #print("I tu")
                        if key[0] == trenutniTuple[0] and key[1].startswith(trenZnStog) and nemaPonavljanja < 1 and key2 == "$" and trenSt not in skupPrihvStanja or (key2 == "$" and trenutniTuple in dictPrijelaza.keys() and "$" in dictPrijelaza[trenutniTuple][key2]):
                            
                            #print(ulSimb)
                            ulazniSimboli.insert(brOcitanihSimbola,ulSimb)
                            
                            #ulSimb = "$"
                            #print(key2)
                            nemaPonavljanja += 1
                            brOcitanihSimbola -=1
                            #print(trenutniTuple)
                        
                            if len(dictPrijelaza[trenutniTuple][key2][1]) != 1 :
                                #stog[-1] = stog[-1][0]
                            
                                stog.append(dictPrijelaza[trenutniTuple][key2][1] + stog[-1][1:])
                            


                            elif len(dictPrijelaza[trenutniTuple][key2][1]) == 1 : 
                                if len(stog[-1]) == 1 :
                                    stog.append(dictPrijelaza[trenutniTuple][key2][1])
                                else :
                                    stog.append(dictPrijelaza[trenutniTuple][key2][1] + stog[-1][1:])
                            

                            if dictPrijelaza[trenutniTuple][key2][1] != "$" :
                                ispis += (dictPrijelaza[trenutniTuple][key2][0] + "#" +stog[-1] + "|" )
                                #print("dodatak ispisu ali u ovom drugom",dictPrijelaza[trenutniTuple][ulSimb][0] + "#" +stog[-1] + "|",brOcitanihSimbola,len(ulazniSimboliPocetni))

                            
                            trenSt =  dictPrijelaza[trenutniTuple][key2][0]
                            trenZnStog = stog[-1][0]
                            #print("TrenZnStog:",trenZnStog)
                            
                            if trenZnStog == "$" :
                                stog.append(stog[-2][1:])
                                #print("Ušao")
                                #print(" stog prije crasha:",stog)
                                if(bool(stog[-1]) == True) :
                                    trenZnStog = stog[-1][0]
                                    ispis += (dictPrijelaza[trenutniTuple][key2][0] + "#" +stog[-1] + "|" )
                                    #print("dodatak ispisu ali u ovom drugom",dictPrijelaza[trenutniTuple][ulSimb][0] + "#" +stog[-1] + "|",brOcitanihSimbola,len(ulazniSimboliPocetni))
                        
                                else :
                                    stog.append("$")
                                    trenZnStog = stog[-1][0]
                                    ispis += (dictPrijelaza[trenutniTuple][key2][0] + "#" +stog[-1] + "|" )
                                    #print("dodatak ispisu ali u ovom drugom",dictPrijelaza[trenutniTuple][ulSimb][0] + "#" +stog[-1] + "|",brOcitanihSimbola,len(ulazniSimboliPocetni))

                            #print(ispis)
                            #print("Novo trenutno(poc) stanje bude:",trenSt, ", novi TrenZnStog je: ",trenZnStog)           
                        else :
                            #tu je besk. petlja
                            
                            break   
                    else:
                        break
            
            elif  trenutniTuple not in dictPrijelaza.keys()  :
                
                ispis +="fail|0"
                break

            elif ulSimb not in dictPrijelaza[trenutniTuple].keys() and ulSimb != "$"   : 
                
                ispis +="fail|0"
                break
            
            
            else:
               
                #ispis+="fail|0"
                break 
        
        
            
        elif ulSimb == ulazniSimboliPocetni[len(ulazniSimboliPocetni) -1] and trenSt in skupPrihvStanja:
            
            #print(ulSimb,trenutniTuple)
            
            ispis +="fail|0"
            break

        else:
            break
        
       
       
    else :
            if stog[-1] == " " :
                
                break 

    if (ispis.endswith("fail|0")) == True:
           
            print(ispis)
    
       
    else :
        #print(ispis)
        zadnjiZapis = ispis.split("|")[-2].split("#")[0]
        zadnjiZnStoga = ispis.split("|")[-2].split("#")[1] 
        
        predzadnjiZapis =   ispis.split("|")[-3].split("#")[0]
        predzadnjiZnStoga = ispis.split("|")[-3].split("#")[1]
        if zadnjiZapis in skupPrihvStanja  : 
            ispis += "1"
            
            if zadnjiZapis == predzadnjiZapis and zadnjiZnStoga == "$" : # vodi do praznog stoga
                ispis = ispis[:-1]
                ispis += "fail|0"
            
                 
       
        elif stog[-1] == "$" and zadnjiZapis in skupPrihvStanja :
            ispis += "fail|0" 
        
            
        else :
            #print(zadnjiZapis,skupPrihvStanja)
            ispis += "0"
        
        #print(ulazniSimboli,ulazniSimboliPocetni)
        print(ispis)
        
        #print(zadnjiZnStoga)
    #print("------")


