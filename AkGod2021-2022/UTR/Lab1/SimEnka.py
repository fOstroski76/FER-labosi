
import string
from sys import stdin
import sys

from numpy import sort


# 1. redak
ulazniNizovi = sys.stdin.readline().strip().split("|")
#print(ulazniNizovi)

#2. redak
lekSkupSt = sys.stdin.readline().strip().split(",")
#print(lekSkupSt)

# 3. redak
skupSimbAbeceda = sys.stdin.readline().strip().split(",")
#print(skupSimbAbeceda)

# 4. redak 
skupPrihvStanja = sys.stdin.readline().strip().split(",")
#print(skupPrihvStanja)

# 5. redak
pocStanje = sys.stdin.readline().strip()
#print(pocStanje)

dictPrijelaza = dict()

# 6. redak nadalje 
for line in sys.stdin:
    sviPrijelazi = line.strip().split("|")
    #print(sviPrijelazi)
    for prijelaz in sviPrijelazi:
        temp = prijelaz.split("->")
        lijevaStr = temp[0]
        desnaStr = temp[1]

        trenutnoStanje = lijevaStr.split(",")[0]
        trenutniZnak = lijevaStr.split(",")[1]

        novaStanja = desnaStr.split(",")

        dictPromjene = dict()
        if trenutnoStanje in dictPrijelaza.keys():
            dictPromjene = dictPrijelaza[trenutnoStanje]
        dictPromjene[trenutniZnak] = novaStanja
        dictPrijelaza[trenutnoStanje] = dictPromjene



       # print("Trenutno:",trenutnoStanje," Zn prijelaza:",trenutniZnak," Nova st:",novaStanja)
       # print("---")
        
#print(dictPrijelaza)        

#print("------")

for ulazniNiz in ulazniNizovi : #  izmedu 2 "|"
    ulazniZnakovi = ulazniNiz.split(",")
    #print("Ulazni znakovi:",ulazniZnakovi)
    output = ""
    trenutnaStanja =set()
    trenutnaStanja.add(pocStanje)
    sljedecaStanja = set()

    for ulazniZnak in ulazniZnakovi:  # izmedu 2 "," 
        if "#" not in trenutnaStanja:   #epsilon prijelazi
           seMijenja = 1
           while seMijenja != 0 :
               novaSt = set()
               seMijenja = 0
               for trenStanje in trenutnaStanja :
                   if trenStanje in dictPrijelaza.keys() :
                       if "$" in dictPrijelaza[trenStanje].keys() :
                           for epsilonStanje in dictPrijelaza.get(trenStanje).get("$") :
                               if epsilonStanje not in trenutnaStanja and  epsilonStanje not in novaSt : # da ne dodaje vise istih stanja
                                   if epsilonStanje != "#" :
                                       novaSt.add(epsilonStanje)
                                       seMijenja = seMijenja + 1
               trenutnaStanja.update(novaSt)
        
        for trenStanje in sorted(trenutnaStanja) :  # dodavanje stanja u ispis
         output = output + trenStanje + ","  
        output = output[:-1] + "|" # uklanjanje "," na  zadnjem dijelu outputa unutar 2 "|" znaka

        if "#" not in trenutnaStanja: # sljedeca stanja
            for trenStanje in trenutnaStanja :
               if trenStanje in dictPrijelaza.keys() :
                   if ulazniZnak in dictPrijelaza[trenStanje].keys() :  
                      for sljedStanje in dictPrijelaza.get(trenStanje).get(ulazniZnak) :
                          if sljedStanje not in sljedecaStanja :
                              if sljedStanje != "#" :
                                  sljedecaStanja.add(sljedStanje)

        sljedecaStanja.discard("#") 
        if not bool(sljedecaStanja) :
            sljedecaStanja.add("#")

        trenutnaStanja.clear()
        trenutnaStanja.update(sljedecaStanja)
        sljedecaStanja.clear()
    
    if "#" not in trenutnaStanja:
        sePromijeni = 1
        while sePromijeni != 0 :
            novaSt = set()
            sePromijeni = 0
            for trenStanje in trenutnaStanja :
                if trenStanje in dictPrijelaza.keys() :
                    if "$" in dictPrijelaza[trenStanje].keys() :
                        for epsilonStanje in dictPrijelaza.get(trenStanje).get("$") :
                               if epsilonStanje not in trenutnaStanja :
                                   if epsilonStanje != "#" :
                                       novaSt.add(epsilonStanje)
                                       sePromijeni = sePromijeni + 1
            trenutnaStanja.update(novaSt)
            

    for trenStanje in sorted(trenutnaStanja) :  
     output = output + trenStanje + ","  
    output = output[:-1] + "|" # uklanjanje "," na  zadnjem dijelu outputa unutar 2 "|" znaka
    print(output[:-1]) # uklanjanje "|" na kraju zadnjeg dijela outputa
   








    
        