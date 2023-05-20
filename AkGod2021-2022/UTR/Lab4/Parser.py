from glob import glob
import string
from sys import stdin
import sys


def sloziIspis(arr):

    ispis = ""
    for el in arr :
        ispis += el
    
    return ispis

index = 0
helpVar = 0
pointlessVar = 0
neCounter = 0

def funkcijaS(inputLista,output,gramatika) :

    global index
    global helpVar
    global pointlessVar
    global neCounter

    output.append("S")
    #print(output)

    if index < len(inputLista) :

        if inputLista[index] == gramatika["S"].split("|")[0][0] : #aAB

            index = index + 1
            funkcijaA(inputLista,output,gramatika)
            funkcijaB(inputLista,output,gramatika)

        elif inputLista[index] == gramatika["S"].split("|")[1][0] : #bBA
            
            index = index + 1
            funkcijaB(inputLista,output,gramatika)
            funkcijaA(inputLista,output,gramatika)

    else :
        pointlessVar = pointlessVar + 1
        print("NE-S")
        #exit()



def funkcijaA(inputLista,output,gramatika) :

    global index
    global helpVar
    global pointlessVar
    global neCounter

    output.append("A")
    #print(output)

    if index < len(inputLista) :

        if inputLista[index] == gramatika["A"].split("|")[0][0] : #bC

            index = index + 1
           
            funkcijaC(inputLista,output,gramatika)
        
        elif inputLista[index] == gramatika["A"].split("|")[1][0] : #a

            index = index + 1
            
            #nista

        else : 
            
            pointlessVar = pointlessVar + 1
            neCounter = neCounter + 1
            #print("NE-A-1")
            

    else : 
        
        #print("NE-A-2")
        if helpVar > 0 :
            
            output.pop()
            #print("helpvar u kodu:",helpVar)
            neCounter = neCounter + 1
        helpVar = helpVar + 1
        
        

def funkcijaB(inputLista,output,gramatika) :

    global index
    global pointlessVar
    global helpVar
    global neCounter
    
    output.append("B")
    #print(output)

    if (1 + index) < len(inputLista) :
        
        if inputLista[index] == gramatika["B"].split("|")[0][0] and inputLista[1 + index] == gramatika["B"].split("|")[0][1] :

            index = index + 2
            funkcijaS(inputLista,output,gramatika)
            

    if (1 + index) < len(inputLista) :
       
        if inputLista[index] == gramatika["B"].split("|")[0][3] and inputLista[1 + index] == gramatika["B"].split("|")[0][4] :
            
            index = index + 2

       

    

def funkcijaC(inputLista,output,gramatika) :

    global index
    global helpVar
    global pointlessVar
    global neCounter
    output.append("C")

    funkcijaA(inputLista,output,gramatika)
    funkcijaA(inputLista,output,gramatika)


#S → aAB | bBA
#A → bC | a
#B → ccSbc | ϵ
#C → AA

gramatika = dict()
gramatika["S"] = "aAB|bBa"
gramatika["A"] = "bC|a"
gramatika["B"] = "ccSbc|ϵ"
gramatika["C"] = "AA"


input = sys.stdin.readline().strip()
#input += "%"  # % = kraj niza
output = list()
inputLista = list()

for char in input :
    #print(char)
    inputLista.append(char)


funkcijaS(inputLista,output,gramatika)
#print(input)
#print(inputLista)
if neCounter == 0:

    print(sloziIspis(output))


elif neCounter != 0 and len(output) > neCounter:

    if neCounter == 1 and helpVar == 2 and output[-1] == "A": # greska pri uklanjanju praznog prelaska u A koji je zadnji, izbrisan clan iz liste
        
        print(sloziIspis(output))
    else :
        print(sloziIspis(output[:-neCounter]))

else :
    
    print(sloziIspis(output[:-1]))

#print("ind:",index," ptsVAR: ",pointlessVar," helpvar:",helpVar)
if index  == len(inputLista)  :
    if helpVar > 0 :
        print("NE")
    else :
        print("DA")

else :
    
    print("NE")

#print(neCounter,helpVar,pointlessVar)
#print(output)
