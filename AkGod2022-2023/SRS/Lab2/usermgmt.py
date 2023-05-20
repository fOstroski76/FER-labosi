#!/usr/bin/env

import argparse
import re
import getpass
import Crypto
import base64
from base64 import encode
from base64 import decode
from Crypto.Random import get_random_bytes
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Hash import SHA256

# definitions

def checkPassStructure (pwd) :

    
    password_pattern = re.compile(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*()_+[\]{};':\"\\|,.<>/?])[A-Za-z\d!@#$%^&*()_+[\]{};':\"\\|,.<>/?]{8,}$")

    if not password_pattern.match(pwd) :
        return False
    
    else :
        return True


# parsing the input 

parser = argparse.ArgumentParser()
group  = parser.add_mutually_exclusive_group()

group.add_argument('--add',type=str)
group.add_argument('--passwrd',type=str)
group.add_argument('--forcepass',type=str)
group.add_argument('--delete',type=str)

args = parser.parse_args()

#print(args)

# actions based on on parsed input 

if args.add :

    #print("Dodavanje usera a?")

    username = args.add
    
    password = getpass.getpass("Password: ")
    password_repeat = getpass.getpass("Repeat password: ")
    print(" ")

    if checkPassStructure(password) and checkPassStructure(password_repeat) :

        if password != password_repeat :

            print("\033[91m[ERROR] : Adding user failed! Passwords mismatch.\033[0m ")
            exit()

        else :  # do stuff

            alreadyExists = False
            

            with open("users.txt",'a+') as users :
                
                users.seek(0)
                allUsers = allUsers = [line.strip() for line in users if line.strip()] #users.readlines() 
                #print(allUsers)

                for us in allUsers :

                    #print(us)
                    storedSalt = base64.b64decode(us.split(" ")[0].encode('ascii'))
                    #storedUsername = base64.b64decode(us.split(" ")[1].encode('ascii'))
                    #print("stored salt:", base64.b64encode(storedSalt).decode('ascii'))

                    userPassToTryFlagZero =  storedSalt + bytes(str(password),'ascii')
                    

                    tryDerivedUsername = PBKDF2(storedSalt + bytes(username,'ascii'), storedSalt, 16,1000000,hmac_hash_module=SHA256)
                    #print("derived username try:",base64.b64encode(tryDerivedUsername).decode('ascii'))
                    tryDerivedKeyZero = PBKDF2(userPassToTryFlagZero, storedSalt, 16,1000000,hmac_hash_module=SHA256)
                    #tryDerivedKeyOne = PBKDF2(userPassToTryFlagOne, storedSalt, 16,1000000,hmac_hash_module=SHA256)
                    
                    #print("us:",us, " tk0: ",base64.b64encode(tryDerivedKeyZero).decode('ascii'), " tk1: ",base64.b64encode(tryDerivedKeyOne).decode('ascii')) 

                    if base64.b64encode(tryDerivedUsername).decode('ascii') == us.split(' ')[1] :
                         
                         alreadyExists = True
                       
                    
                if alreadyExists == True :

                        print("\033[91m[ERROR] : Adding user failed! User already exists!\033[0m")

                else :
                        salt = get_random_bytes(16)

                        saltedUsername = salt + bytes(username,'ascii')
                        saltedStringFlagZero =  salt + bytes(str(password),'ascii')

                        derivedKeyUsername = PBKDF2(saltedUsername, salt, 16, 1000000, hmac_hash_module=SHA256)  
                        derivedKeyFlagZero = PBKDF2(saltedStringFlagZero, salt, 16, 1000000, hmac_hash_module=SHA256) 

                        #users.write(str(username + ' ' + password + ' ' + '0'))  # 0/1 will be flags for forcepass
                        users.write(base64.b64encode(salt).decode('ascii') + " " + base64.b64encode(derivedKeyUsername).decode('ascii') + " " + base64.b64encode(derivedKeyFlagZero).decode('ascii') + " " + "0")  
                        users.write('\n')

                        print("\033[92m[USERMGMT] : User {} successfully added.\033[0m".format(username))
            

             
          
    else :

        print("\033[91m[ERROR] : Adding user failed! Password(s) too weak!\033[0m")
        print(" ")
        print("Please follow these rules when creating a password:")
        print("Password must contain at least 8 characters including at least one uppercase letter, one lowercase letter, one digit, and one special character (!@#$%^&*()_+[]{};':\"\\|,.<>/?).")
        exit()


if args.passwrd :
                                
    username = args.passwrd   # otvori datoteku, najdi user, promeni pass

    allUsers = list()       

    with open("users.txt",'r+') as users :

        allUsers = allUsers = [line.strip() for line in users if line.strip()] #users.readlines()
        exists  = False

        for us in allUsers :


            storedSalt = base64.b64decode(us.split(" ")[0].encode('ascii'))
            tryDerivedUsername = PBKDF2(storedSalt + bytes(username,'ascii'), storedSalt, 16,1000000,hmac_hash_module=SHA256)
             

            if base64.b64encode(tryDerivedUsername).decode('ascii') == us.split(' ')[1] :
                         
                exists = True
            
        
        if exists == False :

             print("\033[91m[ERROR] : User doesnt exist!\033[0m")
        
        else :

            #users.close()
            print("[USERMGMT] : Please enter your new desired password.")

            password = getpass.getpass("New password: ")
            password_repeat = getpass.getpass("Repeat new password: ")
            print(" ")

            if checkPassStructure(password) and checkPassStructure(password_repeat) :

                if password != password_repeat :

                    print("\033[91m[ERROR] : Password change failed! Passwords mismatch.\033[0m ")
                    exit()
        
                else : # do stuff
                    newListAllUsers = list()
                    for u in allUsers :

                        #print(us)
                        storedSalt = base64.b64decode(u.split(" ")[0].encode('ascii'))
                        tryDerivedUsername = PBKDF2(storedSalt + bytes(username,'ascii'), storedSalt, 16,1000000,hmac_hash_module=SHA256)
                    
                        #print("us:",us, " tk0: ",base64.b64encode(tryDerivedKeyZero).decode('ascii'), " tk1: ",base64.b64encode(tryDerivedKeyOne).decode('ascii')) 

                        if base64.b64encode(tryDerivedUsername).decode('ascii') == u.split(' ')[1] :
                            
                            #newSalt = get_random_bytes(16)
                            newhashedPass = storedSalt + bytes(str(password),'ascii')
                            newPass = PBKDF2(newhashedPass ,storedSalt, 16, 1000000, hmac_hash_module=SHA256)
                            #print(base64.b64encode(newPass).decode('ascii'))
                            newListAllUsers.append(base64.b64encode(storedSalt).decode('ascii') + " " + base64.b64encode(tryDerivedUsername).decode('ascii') + " " + base64.b64encode(newPass).decode('ascii')+ " " + u.split(' ')[3])

                        else :
                            newListAllUsers.append(u)
                        #print(newListAllUsers)

                    with open("users.txt",'w+') as newUsers :

                        for el in newListAllUsers :
                            newUsers.write(el)
                            newUsers.write('\n')
                    
                    newUsers.close()

                    print("\033[92m[USERMGMT] : Password successfully changed.\033[0m")

            else :

                print("\033[91m[ERROR] : Changing password failed! Password(s) too weak!\033[0m")
                print(" ")
                print("Please follow these rules when creating a password:")
                print("Password must contain at least 8 characters including at least one uppercase letter, one lowercase letter, one digit, and one special character (!@#$%^&*()_+[]{};':\"\\|,.<>/?).")
                exit()


if args.forcepass :

    username = args.forcepass

    allUsers = list()

    with open("users.txt",'r+') as users :

        allUsers = allUsers = [line.strip() for line in users if line.strip()] #users.readlines()
        exists  = False

        for us in allUsers :
            
            storedSalt = base64.b64decode(us.split(" ")[0].encode('ascii'))
            tryDerivedUsername = PBKDF2(storedSalt + bytes(username,'ascii'), storedSalt, 16,1000000,hmac_hash_module=SHA256)
             

            if base64.b64encode(tryDerivedUsername).decode('ascii') == us.split(' ')[1] :
                         
                exists = True
        
        if exists == False :

             print("\033[91m[ERROR] : User doesnt exist!\033[0m")
        
        else :
            
            newListAllUsers = list()

            for u in allUsers :

                storedSalt = base64.b64decode(u.split(" ")[0].encode('ascii'))
                tryDerivedUsername = PBKDF2(storedSalt + bytes(username,'ascii'), storedSalt, 16,1000000,hmac_hash_module=SHA256)
             

                if base64.b64encode(tryDerivedUsername).decode('ascii') == u.split(' ')[1] :
                         
                    newListAllUsers.append(u.split(' ')[0] + " " + u.split(' ')[1] + " " + u.split(' ')[2] + " " + "1")

                else :

                    newListAllUsers.append(u)


            with open("users.txt",'w+') as newUsers :

                        for el in newListAllUsers :
                            newUsers.write(el)
                            newUsers.write('\n')
                    
            newUsers.close()    

            print("\033[92m[USERMGMT] : User will be requested to change their password on next login.\033[0m")


if args.delete : 

    username  = args.delete

    with open("users.txt",'r+') as users :

        allUsers = [line.strip() for line in users if line.strip()] #users.readlines()
        exists  = False

        for us in allUsers :
            
            storedSalt = base64.b64decode(us.split(" ")[0].encode('ascii'))
            tryDerivedUsername = PBKDF2(storedSalt + bytes(username,'ascii'), storedSalt, 16,1000000,hmac_hash_module=SHA256)
             

            if base64.b64encode(tryDerivedUsername).decode('ascii') == us.split(' ')[1] :
                         
                exists = True

        if exists == False :

            print("\033[91m[ERROR] : User doesnt exist!\033[0m")
        
        else :
             
            
            newListAllUsers = list()

            for u in allUsers :

                storedSalt = base64.b64decode(u.split(" ")[0].encode('ascii'))
                tryDerivedUsername = PBKDF2(storedSalt + bytes(username,'ascii'), storedSalt, 16,1000000,hmac_hash_module=SHA256)
             

                if base64.b64encode(tryDerivedUsername).decode('ascii') == u.split(' ')[1] :
                         
                    pass

                else :

                    newListAllUsers.append(u)


            with open("users.txt",'w+') as newUsers :

                        for el in newListAllUsers :
                            newUsers.write(el)
                            newUsers.write('\n')
                    
            newUsers.close()

            print("\033[92m[USERMGMT] : User {} successfully deleted.\033[0m".format(username))    
             
            