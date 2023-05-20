#!/usr/bin/env

import Crypto
import sys
from sys import stdin
from base64 import b64encode
from base64 import b64decode
from Crypto.Cipher import AES
from Crypto.Cipher import _mode_gcm
from Crypto.Hash import SHA256
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Random import get_random_bytes


def runLogFile() :  # za debugganje
    logFile = open("log.txt","a")   



    logFile.write("------")
    logFile.write('\n')
    
    
    for line in documentLines[1:] :
        logFile.write(line)
        logFile.write('\n') # prva testiranja

def printMsg(num) : 

    if num == 1 :
    
        print(" ")
        print(" ")
        print("Welcome to the Password manager! Following options are:")
        print(" ")
        print("1.Clear passwords database and initialize a new Password manager with a new master password(keyword:init)")
        print("2. Add a new address-password pair (keyword:put)")
        print("3. Check password for an existing address (keyword:get)")
        print(" ")
        print("-----------------------------------------------------------------------------------------------")
        print("For option 1, follow this command template:")
        print("$ python3 PasswordManager.py init [new_master_password]")
        print("For option 2, follow this command template:")
        print("$ python3 PasswordManager.py put [master_password] [desired_address] [desired_password]")
        print("For option 3, follow this command template:")
        print("$ python3 PasswordManager.py get [master_password] [desired_address]")
        print(" ")
        print("To show  these commands again, type:")
        print("$ python3 PasswordManager.py help")
        print("-----------------------------------------------------------------------------------------------")
        print(" ")
        print("To begin, please initialize a password database with >init< command.")
        print(" ")
        print("NOTE: any other command combination will cause program to not work properly or cause errors")
        print(" ")
        print(" ")
        print(" ")

    elif num == 2 :

        print(" ")
        print("1.Clear passwords database and initialize a new Password manager with a new master password(keyword:init)")
        print("2. Add a new address-password pair (keyword:put)")
        print("3. Check password for an existing address (keyword:get)")
        print(" ")
        print("-----------------------------------------------------------------------------------------------")
        print("For option 1, follow this command template:")
        print("$ python3 PasswordManager.py init [new_master_password]")
        print("For option 2, follow this command template:")
        print("$ python3 PasswordManager.py put [master_password] [desired_address] [desired_password]")
        print("For option 3, follow this command template:")
        print("$ python3 PasswordManager.py get [master_password] [desired_address]")
        print(" ")
        

documentLines = sys.argv
#print(documentLines)

try :
    masterpass = sys.argv[2]  # 1 je "Init" , to u uputama napiši da se pokreće sa init
    mp_salt = get_random_bytes(16)
    #print("[DEBUG] Salt za key: ",b64encode(mp_salt).decode('ascii'), " plain oblik: ",mp_salt)
    mp_generated_key = PBKDF2(masterpass,mp_salt,16,10000,hmac_hash_module=SHA256)
    #print("[DEBUG] Key from MP:",b64encode(mp_generated_key).decode('ascii))
    print(" ")

except (IndexError) :
    pass

#runLogFile() 


if documentLines[1] == "start" and len(documentLines) == 2 :

    printMsg(1)
    storedPassesFile = open("storedPasswordsFile.txt","a+")
    storedPassesFile.close()

elif documentLines[1] == "help" and len(documentLines) == 2 :

    printMsg(2)

elif documentLines[1] == "init" and len(documentLines) == 3 :

    masterpass = sys.argv[2] 
    
    storedPassesFile = open("storedPasswordsFile.txt","a+")
    storedPassesFile.close()

    storedPassesFile = open("storedPasswordsFile.txt","w")
    storedPassesFile.close()

    print("Password manager initialized.")
    
      

elif documentLines[1] == "put" :
    if len(documentLines) != 5 :  
        print("Incorrect input!")
        exit()
        
    else:

        # normalan rad programa
        masterpass = sys.argv[2]  # 1 je "Init" , to u uputama napiši da se pokreće sa init
        mp_salt = get_random_bytes(16)
        #print("[DEBUG] Salt za key: ",b64encode(mp_salt).decode('ascii'), " plain oblik: ",mp_salt)
        mp_generated_key = PBKDF2(masterpass,mp_salt,16,10000,hmac_hash_module=SHA256)
        #print("[DEBUG] Key from MP:",b64encode(mp_generated_key).decode('ascii'))
        iv = get_random_bytes(16)
        #print("[DEBUG] generirani iv: ",b64encode(iv).decode('ascii'))
        #print(" ")
        
        
        newAddress = documentLines[3]
        storedPassesFile = open("storedPasswordsFile.txt","r+")
        passSearchDict = dict()
        lines = storedPassesFile.readlines()
        #print(lines)
        try :
            for line in lines :
                #print("Lajna: ",line[0:24]," ",line[25:49]," ",line[50:74]," ",line[75:])
                decrypt_salt = line[0:24]
                decrypt_iv = line[24:48]
                keyValuePair = line[72:]
                onaj_tag = line[48:72]
                #print("decr. salt: ",decrypt_salt," decr. iv: ",decrypt_iv," kv pair: ",keyValuePair)

                regenerated_key_with_mp = PBKDF2(masterpass,b64decode(decrypt_salt),16,10000,hmac_hash_module=SHA256)
                #print("ponovno generirani mp key: ",b64encode(regenerated_key_with_mp).decode('ascii'))

                cipher_decyrpt = AES.new(regenerated_key_with_mp,AES.MODE_GCM,nonce=b64decode(decrypt_iv))
                dekriptirani_ciphertext = cipher_decyrpt.decrypt_and_verify(b64decode(keyValuePair),b64decode(onaj_tag))

                #print("Dek. ct: ",dekriptirani_ciphertext[16:].decode('ascii'))
                desiredAddress_back_as_a_string = dekriptirani_ciphertext[16:].decode('ascii')
                passSearchDict[desiredAddress_back_as_a_string.split(" ")[0]] = desiredAddress_back_as_a_string.split(" ")[1]
                #print(passSearchDict)
        

            if newAddress in passSearchDict :

                for key in passSearchDict.keys() :
                        if key == newAddress :
                            passSearchDict[key] = documentLines[4]


                storedPassesFile.close()

                storedPassesFile = open("storedPasswordsFile.txt","a+")

                for key in passSearchDict.keys() :
                    if key == newAddress :

                        newInput = "{}{}{}".format(newAddress," ",passSearchDict[key])
                        newInput_as_bytes = bytes(newInput,'ascii')
                        newInput_as_bytes = get_random_bytes(16) + newInput_as_bytes

                        cypher_encrypt = AES.new(mp_generated_key,AES.MODE_GCM,nonce=iv)
                        cyphertext_NewInput_as_bytes , tag = cypher_encrypt.encrypt_and_digest(newInput_as_bytes)

                        finalNewInput = "{}{}{}{}".format(b64encode(mp_salt).decode('ascii'),b64encode(iv).decode('ascii'),b64encode(tag).decode('ascii'),b64encode(cyphertext_NewInput_as_bytes).decode('ascii'))

                        storedPassesFile.write(finalNewInput)
                        storedPassesFile.write('\n')
                        print("Stored password for: {}.".format(newAddress))
                        storedPassesFile.close()
                #print(passSearchDict)
                #print("Updateana šifra za adresu: ",newAddress)
                
            else :


                storedPassesFile = open("storedPasswordsFile.txt","a+")
            
                newPass = documentLines[4]
            
                newInput = "{}{}{}".format(newAddress," ",newPass)
                newInput_as_bytes = bytes(newInput,'ascii')
                newInput_as_bytes = get_random_bytes(16) + newInput_as_bytes

                cypher_encrypt = AES.new(mp_generated_key,AES.MODE_GCM,nonce=iv)
                cyphertext_NewInput_as_bytes , tag = cypher_encrypt.encrypt_and_digest(newInput_as_bytes)
                #print("[DEBUG] cyphertext: ",b64encode(cyphertext_NewInput_as_bytes).decode('ascii'))
                #print("[DEBUG] tag: ",b64encode(tag).decode('ascii'))
                #print(" ")
                #print("[DEBUG] Format ispisa je: salt:iv:kriptirani par adresa:sifra")
                finalNewInput = "{}{}{}{}".format(b64encode(mp_salt).decode('ascii'),b64encode(iv).decode('ascii'),b64encode(tag).decode('ascii'),b64encode(cyphertext_NewInput_as_bytes).decode('ascii'))
            
                storedPassesFile.write(finalNewInput)
                storedPassesFile.write('\n')
                print("Stored password for: {}.".format(newAddress))
                storedPassesFile.close()

        except (KeyError, ValueError):
            print("Incorrect master password or integrity check failed!")
    
            
    
elif documentLines[1] == "get" :
    
    if len(documentLines) != 4 :
        print("Incorrect input!")
        exit()

    else:
        #normalan rad programa

        storedPassesFile = open("storedPasswordsFile.txt","r+")
        desiredAddress = documentLines[3]
        passSearchDict = dict()

        # dekriptiraj ono iz datoteke
        try :

            lines = storedPassesFile.readlines()
        #print("U datoteci:")
            for line in lines :
                #print("NOVA LINIJA: ",line[:-1])
                decrypt_salt = line[0:24]
                decrypt_iv = line[24:48]
                keyValuePair = line[72:]
                onaj_tag = line[48:72]
                #print("decr. salt: ",decrypt_salt," decr. iv: ",decrypt_iv," kv pair: ",keyValuePair)

                regenerated_key_with_mp = PBKDF2(masterpass,b64decode(decrypt_salt),16,10000,hmac_hash_module=SHA256)
                #print("ponovno generirani mp key: ",b64encode(regenerated_key_with_mp).decode('ascii'))

                cipher_decyrpt = AES.new(regenerated_key_with_mp,AES.MODE_GCM,nonce=b64decode(decrypt_iv))
                dekriptirani_ciphertext = cipher_decyrpt.decrypt_and_verify(b64decode(keyValuePair),b64decode(onaj_tag))

                #print("Dek. ct: ",dekriptirani_ciphertext[16:].decode('ascii'))
                desiredAddress_back_as_a_string = dekriptirani_ciphertext[16:].decode('ascii')
                passSearchDict[desiredAddress_back_as_a_string.split(" ")[0]] = desiredAddress_back_as_a_string.split(" ")[1]

            #print(passSearchDict)
            for key in passSearchDict.keys() :
                if key == desiredAddress :
                    print("Password for {} is {}.".format(key,passSearchDict[key]))

            storedPassesFile.close()

        except (KeyError, ValueError) :  
            print("Incorrect Master password or integrity check failed!")
            

else:
    print("Incorrect input!")
    exit()
        
"""
print(" ")
print("[DEBUG] ",documentLines)

try :
    print("[DEBUG] MP:",masterpass)
except(NameError) :
    pass

print(" ")
print(" ")
"""

if __name__ == "__main__ " :
    print("[DEBUG] Šifre u datoteci:")
    storedPassesFile = open("storedPasswordsFile.txt","r+")
    print(storedPassesFile.read())