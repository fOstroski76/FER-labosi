import string
from sys import stdin
import sys
import numpy as np


def izbaciNedohvatljivaStanja(lekSkupSt,skupSimbAbeceda,dictPrijelaza,dictPromjene,pocStanje,dohvStanja) :
    #print("Trenutno poc stanje je:",pocStanje)
    
    if pocStanje in dictPrijelaza.keys():
        for simbol in skupSimbAbeceda :
            #print("Trenutni simbol je:",simbol)
            if simbol in dictPrijelaza[pocStanje].keys() and dictPrijelaza[pocStanje][simbol] not in dohvStanja : 
                dohvStanja.append(dictPrijelaza[pocStanje][simbol])
                x=dictPrijelaza[pocStanje][simbol]
                #print("Dohvatljivo stanje je:",x)
                return izbaciNedohvatljivaStanja(lekSkupSt,skupSimbAbeceda,dictPrijelaza,dictPromjene,x,dohvStanja)
    return dohvStanja


# ucitavanje varijabli 

# 1. redak
lekSkupSt = sys.stdin.readline().strip().split(",")
#print(lekSkupSt)

# 2. redak
skupSimbAbeceda = sys.stdin.readline().strip().split(",")
#print(skupSimbAbeceda)

# 3. redak 
skupPrihvStanja = sys.stdin.readline().strip().split(",")
#print(skupPrihvStanja)

# 4. redak
pocStanje = sys.stdin.readline().strip()
#print(pocStanje)

dictPrijelaza = dict()

# 5. i svi ostali retci

for line in sys.stdin:
    sviPrijelazi = line.strip().split("->")
    #print(sviPrijelazi)
    lijevaStr = sviPrijelazi[0]
    desnaStr = sviPrijelazi[1]

    trenutnoStanje = lijevaStr.split(",")[0]
    trenutniSimbol = lijevaStr.split(",")[1]
    iduceStanje = desnaStr

    dictPromjene = dict()
    if trenutnoStanje in dictPrijelaza.keys() :
        dictPromjene = dictPrijelaza[trenutnoStanje]
    dictPromjene[trenutniSimbol] = iduceStanje
    dictPrijelaza[trenutnoStanje] = dictPromjene

    #print("Trenutno:",trenutnoStanje," Simbol prijelaza:",trenutniSimbol," Iduce st:",iduceStanje)
#print("---") 
#print(dictPrijelaza)

#  glavna logika programa

 # uklanjanje nedohvatljivih stanja
dohvStanja = list()    
dohvStanja.append(pocStanje)
for stanje in lekSkupSt :
    izbaciNedohvatljivaStanja(lekSkupSt,skupSimbAbeceda,dictPrijelaza,dictPromjene,pocStanje,dohvStanja)
#print(sorted(dohvStanja))

# uklanjanje istovjetnih stanja

brSt = len(dohvStanja)
#print(brSt)
tablica = np.ones((brSt,brSt), dtype = int)
dohvStanja.sort()
# za tablicu nam treba samo donja trokutasta matrica pa ostale elemente stavljamo na 0, 
# ono sto na kraju ostane 1 su istovjetna stanja

for i in range (brSt) :
    for j in range (brSt) :
        if i<=j : tablica[i][j] = 2 # ovo imas za lakse gledanje, vrati na 0!

# odmah prekrizimo prijelaze vezana za prihvatljiva stanja jer neprihvatljiva ne mogu biti istovjetna s tim
for i in range (brSt) :
    for j in range (brSt) :
        if i>j :
            if (dohvStanja[i] in skupPrihvStanja and dohvStanja[j] not in skupPrihvStanja)  or (dohvStanja[j] in skupPrihvStanja and dohvStanja[i] not in skupPrihvStanja):
                tablica[i][j] = 0
#print(tablica)
#print("----------------")

dictPracenjaStanja = dict()
for i in range (brSt) :
    for j in range (brSt) :
        if i>j and tablica[i][j] == 1 :
            for simbol in skupSimbAbeceda :
                #print("Trenutni simbol:",simbol)
                if ((dictPrijelaza[dohvStanja[i]][simbol] in skupPrihvStanja) and (dictPrijelaza[dohvStanja[j]][simbol] not in skupPrihvStanja)) or ((dictPrijelaza[dohvStanja[i]][simbol]  not in skupPrihvStanja) and (dictPrijelaza[dohvStanja[j]][simbol]  in skupPrihvStanja)) :
                    tablica[i][j] = 0
                    #print("Oznacio sam polje tablica[",i,"][",j,"]")
                    #ako u su u dictu pod keyom koji su ta dva stanja upisana neka stanja, njih krizaj!
                    tempTuple2 = (dohvStanja[i],dohvStanja[j])
                    if  tempTuple2 in dictPracenjaStanja.keys():
                        for k in range (brSt) :
                            for l in range (brSt) :
                                if dohvStanja[k] == dictPracenjaStanja[tempTuple2][0] and dohvStanja[l] == dictPracenjaStanja[tempTuple2][1] :
                                    tablica[k][l] = 0
                                    #print("Prekrizio  sam dodatno i polje tablica[",k,"][",l,"]")
                         
                else : 
                    for simbol in skupSimbAbeceda :
                        if dictPrijelaza[dohvStanja[i]][simbol] != dictPrijelaza[dohvStanja[j]][simbol] :
                            tuplePrijelaza = (dictPrijelaza[dohvStanja[i]][simbol],dictPrijelaza[dohvStanja[j]][simbol])
                            tuplePocetni = (dohvStanja[i],dohvStanja[j])
                            dictPracenjaStanja[tuplePrijelaza] =  tuplePocetni
                    #print(dictPracenjaStanja)
                   

"""print("-------------------")
print("Tablica nakon edita:")
print(tablica)                    
print(dictPracenjaStanja)"""

# zamjena istovjetnih stanja leksicki manjim stanjima 

konacnaStanja = list()
suvisnaStanja = list()
for i in range (brSt) :
    for j in range (brSt) :
        if i>j and tablica[i][j] == 1 :
            #print("Istovjetna stanja su:",dohvStanja[i],",",dohvStanja[j])
            if (dohvStanja[i] < dohvStanja[j]) : 
                if dohvStanja[i] not in konacnaStanja :
                    konacnaStanja.append(dohvStanja[i])
                if dohvStanja[j] not in suvisnaStanja :
                    suvisnaStanja.append(dohvStanja[j])
                
            else :
                if dohvStanja[j] not in konacnaStanja :
                    konacnaStanja.append(dohvStanja[j])
                if dohvStanja[i] not in suvisnaStanja :
                    suvisnaStanja.append(dohvStanja[i])
                
#print("Konacna st:",konacnaStanja) 
#print("Suvisna st:",suvisnaStanja)

for st in konacnaStanja :
    if st in konacnaStanja and st in suvisnaStanja :
        konacnaStanja.remove(st)
        #print("Brisem:",st)

konacnaStanja.sort()
#print("Nova kon stanja:",konacnaStanja)

for sta in dohvStanja :
    if sta not in konacnaStanja and sta not in suvisnaStanja :
        konacnaStanja.append(sta)
        #print("Dodajem st:",st)

for st in konacnaStanja :
    if st in konacnaStanja and st in suvisnaStanja :
        konacnaStanja.remove(st)
        #print("Brisem:",st)

for st in konacnaStanja :
    if st in konacnaStanja and st in suvisnaStanja :
        konacnaStanja.remove(st)
        #print("Brisem:",st)

konacnaStanja.sort()
  

#print(konacnaStanja)
for i in range (brSt) :
    for j in range (brSt) :
        if i>j and tablica[i][j] == 1 :
            if (dohvStanja[i] < dohvStanja[j]) : 
                if pocStanje == dohvStanja[j] :
                    pocStanje = dohvStanja[i]
                for stanje in konacnaStanja :
                    for simbol in skupSimbAbeceda :
                        if simbol in dictPrijelaza[stanje].keys() :
                            if dictPrijelaza[stanje][simbol] == dohvStanja[j] :
                                dictPrijelaza[stanje][simbol] = dohvStanja[i]
            else :
                if pocStanje == dohvStanja[i] :
                    pocStanje = dohvStanja[j]
                for stanje in konacnaStanja :
                    for simbol in skupSimbAbeceda :
                        if simbol in dictPrijelaza[stanje].keys() :
                            if dictPrijelaza[stanje][simbol] == dohvStanja[i] :
                                dictPrijelaza[stanje][simbol] = dohvStanja[j] 


# konacni ispis
#print("Konacni ispis:")
outputl1 = ""

for stanje in konacnaStanja :
    outputl1 += stanje 
    outputl1 += ","
print(outputl1[:-1])

outputl2 = ""
for simbol in skupSimbAbeceda :
    outputl2 += simbol 
    outputl2 += ","
print(outputl2[:-1])

outputl3 = ""
for stanje in skupPrihvStanja :
    if stanje in konacnaStanja :
        outputl3 += stanje
        outputl3 += ","
print(outputl3[:-1]) 
print(pocStanje) #outputl4

#output lineovi 5 nadalje :
#print(dictPrijelaza)
for stanje in konacnaStanja :
    for simbol in skupSimbAbeceda :
        if stanje in dictPrijelaza.keys() : 
            outputlx = ""
            outputlx += stanje
            outputlx += ","
            outputlx += simbol
            outputlx +="->"
            outputlx += dictPrijelaza[stanje][simbol]
            print(outputlx)

#print(dictPrijelaza['p1'].keys())