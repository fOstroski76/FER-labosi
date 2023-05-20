#!/usr/bin/env

import getpass
import Crypto
import re
import argparse
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
    

def passwordChangeCheck(newPassword, newPassword_repeat) :
    

    if newPassword != newPassword_repeat :
        return False
    
    
    if checkPassStructure(newPassword) == False or checkPassStructure(newPassword_repeat) == False :
        return False
    
    return True

# parsing input    

parser = argparse.ArgumentParser()
parser.add_argument('--login',type=str)

args =  parser.parse_args()

#print(args)


if args.login :

    username = args.login

    exists = False
    needsToChangePass = False
    wrongPass = False
    notOldPass = True

    password = getpass.getpass("Password: ")

    with open("users.txt",'a+') as users :

        users.seek(0)

        allUsers = allUsers = [line.strip() for line in users if line.strip()] #users.readlines() 
                #print(allUsers)

        for us in allUsers :

            storedSalt = base64.b64decode(us.split(" ")[0].encode('ascii'))
            tryDerivedUsername = PBKDF2(storedSalt + bytes(username,'ascii'), storedSalt, 16,1000000,hmac_hash_module=SHA256)
            userPassToTryFlagZero =  storedSalt + bytes(str(password),'ascii')
            tryDerivedKeyZero = PBKDF2(userPassToTryFlagZero, storedSalt, 16,1000000,hmac_hash_module=SHA256) 

            if base64.b64encode(tryDerivedUsername).decode('ascii') == us.split(' ')[1] :
                         
                exists = True
            
                if us.split(' ')[3] == "1" :
                    needsToChangePass = True
                
                if base64.b64encode(tryDerivedKeyZero).decode('ascii') != us.split(' ')[2] :
                    wrongPass = True


    users.close()

    if exists == False or wrongPass == True :

        print("\033[91m[ERROR] : Login failed!\033[0m")
        exit()
    

    elif needsToChangePass == True :
        print("\033[93m[LOGIN] : Login successful, however, administrators have requested immediate password change.\033[0m")

        newPassword = getpass.getpass("New password: ")
        newPassword_repeat = getpass.getpass("Repeat new password: ")
        oldPasswordKDF = " "
        
        with open("users.txt",'r+') as users :

            allUsers = allUsers = [line.strip() for line in users if line.strip()] #users.readlines()
        
            for us in allUsers :
                
                storedSalt = base64.b64decode(us.split(" ")[0].encode('ascii'))
                tryDerivedUsername = PBKDF2(storedSalt + bytes(username,'ascii'), storedSalt, 16,1000000,hmac_hash_module=SHA256)
                userPassToTryFlagZero =  storedSalt + bytes(str(password),'ascii')
                tryDerivedKeyZero = PBKDF2(userPassToTryFlagZero, storedSalt, 16,1000000,hmac_hash_module=SHA256) 

                if base64.b64encode(tryDerivedUsername).decode('ascii') == us.split(' ')[1] :
                         
                    newSaltedPass = storedSalt + bytes(str(newPassword),'ascii')
                    newPassKDF = PBKDF2(newSaltedPass, storedSalt, 16,1000000,hmac_hash_module=SHA256)

                    if  base64.b64encode(newPassKDF).decode('ascii') == us.split(' ')[2] :

                        notOldPass = False
            
                

            if passwordChangeCheck(newPassword,newPassword_repeat) ==  True and notOldPass == True :

                newListAllUsers = list()
                for u in allUsers :
                    
                    storedSalt = base64.b64decode(us.split(" ")[0].encode('ascii'))
                    tryDerivedUsername = PBKDF2(storedSalt + bytes(username,'ascii'), storedSalt, 16,1000000,hmac_hash_module=SHA256)
                    newPassToStore =  storedSalt + bytes(str(newPassword),'ascii')
                    newPassDerivedKey = PBKDF2(newPassToStore, storedSalt, 16,1000000,hmac_hash_module=SHA256) 

                    if base64.b64encode(tryDerivedUsername).decode('ascii') == u.split(' ')[1] :
                         
                        newListAllUsers.append(base64.b64encode(storedSalt).decode('ascii') + " " + base64.b64encode(tryDerivedUsername).decode('ascii') + " " + base64.b64encode(newPassDerivedKey).decode('ascii') + " " + "0")
                    
                    else :

                        newListAllUsers.append(u)


                #print(newListAllUsers)

                with open("users.txt",'w+') as newUsers :

                    for el in newListAllUsers :
                        newUsers.write(el)
                        newUsers.write('\n')
                    
                newUsers.close()

                print("\033[92m[LOGIN] : Password change successful.\033[0m")

            else:
                while passwordChangeCheck(newPassword,newPassword_repeat) ==  False or notOldPass == False:

                    notOldPass = True

                    print("\033[91m[ERROR] : Password change failed! Please try again.\033[0m")
                    
                    print(" ")
                    newPassword = getpass.getpass("New password: ")
                    newPassword_repeat = getpass.getpass("Repeat new password: ")

                    for us in allUsers :
                
                        storedSalt = base64.b64decode(us.split(" ")[0].encode('ascii'))
                        tryDerivedUsername = PBKDF2(storedSalt + bytes(username,'ascii'), storedSalt, 16,1000000,hmac_hash_module=SHA256)
                        userPassToTryFlagZero =  storedSalt + bytes(str(password),'ascii')
                        tryDerivedKeyZero = PBKDF2(userPassToTryFlagZero, storedSalt, 16,1000000,hmac_hash_module=SHA256) 

                        if base64.b64encode(tryDerivedUsername).decode('ascii') == us.split(' ')[1] :
                         
                            newSaltedPass = storedSalt + bytes(str(newPassword),'ascii')
                            newPassKDF = PBKDF2(newSaltedPass, storedSalt, 16,1000000,hmac_hash_module=SHA256)

                            if  base64.b64encode(newPassKDF).decode('ascii') == us.split(' ')[2] :

                                notOldPass = False

                    passwordChangeCheck(newPassword,newPassword_repeat)


                newListAllUsers = list()
                for u in allUsers :
                    
                    storedSalt = base64.b64decode(us.split(" ")[0].encode('ascii'))
                    tryDerivedUsername = PBKDF2(storedSalt + bytes(username,'ascii'), storedSalt, 16,1000000,hmac_hash_module=SHA256)
                    newPassToStore =  storedSalt + bytes(str(newPassword),'ascii')
                    newPassDerivedKey = PBKDF2(newPassToStore, storedSalt, 16,1000000,hmac_hash_module=SHA256) 

                    if base64.b64encode(tryDerivedUsername).decode('ascii') == u.split(' ')[1] :
                         
                        newListAllUsers.append(base64.b64encode(storedSalt).decode('ascii') + " " + base64.b64encode(tryDerivedUsername).decode('ascii') + " " + base64.b64encode(newPassDerivedKey).decode('ascii') + " " + "0")
                    
                    else :

                        newListAllUsers.append(u)


                #print(newListAllUsers)

                with open("users.txt",'w+') as newUsers :

                    for el in newListAllUsers :
                        newUsers.write(el)
                        newUsers.write('\n')
                    
                newUsers.close()
                
                print("\033[92m[LOGIN] : Password change successful.\033[0m")
        
    else :
        print("\033[92m[LOGIN] : Login successful.\033[0m")



    

