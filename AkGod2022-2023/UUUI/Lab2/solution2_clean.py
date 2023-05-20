import argparse


# definitons 

class Clause :

    def __init__(self, literals, parents) :

        self.literals = literals
        self.parents = parents

    
    def printAttrs (self) :
        
        try :
            if len(self.literals) != 0 :
                print("Clause: {} <-- from : ({} and {})".format(self.literals,self.parents[0].literals , self.parents[1].literals))

            else :
                print("Clause: NIL <-- from : ({} and {})".format(self.parents[0].literals , self.parents[1].literals))

        except (AttributeError):
            pass
    
    


def negatify (input) :
    split_input = input.split(' ')
    print(" ")
    
    if len(split_input) == 1 : # one literal
        if split_input[0].startswith("~") :

            return split_input[0][1:]
        else :

            return "~" + split_input[0]

    elif len(split_input) != 0 and len(split_input) > 1 : # more literals
        
        return "~(" + input + ")"
    

def initialRedundancyCheck(clausesList,isCooking) :
    somethingRemoved  = False

    if isCooking == False :
        print("=== Redundancy check: ====")

    for cla in clausesList :        # tautology check
        positive = set()
        negative = set()

        for el in cla.split(' ') :

            if el == "v" or el == "V" :
                pass
            
            else :
                if el.startswith("~") :
                    negative.add(el[1:])

                else :
                    positive.add(el)

        for literal in positive :
            if literal in negative :
                somethingRemoved = True

                if isCooking == False :
                    print("Removed: ({}) : (tautology)".format(cla))

                temp = cla.split(' ')
                for t in temp :
                    if t == "v" or t == "V" :
                        temp.remove(t)

                clausesList.remove(cla)


                                            
    for cla in clausesList :            # supersets check
        for cla2 in clausesList :
            if cla != cla2 :
                  if set(cla.split(' ')).issubset(cla2.split(' ')) : 
                    if isCooking == False :
                        print("Removed ({}) : All elements from ({}) are in ({})!".format(cla2,cla,cla2))

                    temp2 = cla2.split(' ')
                    for t in temp2 :
                        if t == "v" or t == "V" :
                            temp2.remove(t)
                    
                     
                    clausesList.remove(cla2)
                    somethingRemoved = True           
        

    if somethingRemoved == False and isCooking == False :
        print("Nothing was removed")

    if isCooking == False :    
        print("==========================")


def RedundancyCheck(resolvents,usableClauseDict) :
    
    positiveEls = set()
    negativeEls = set()
    usableClauseDictCopy  = usableClauseDict.copy()
    
    for el in resolvents :
        if el.startswith("~") :
            negativeEls.add(el[1:])
        
        else :
            positiveEls.add(el)
    
    for el in resolvents :
        if el in positiveEls and el in negativeEls :
            return False

    for el in usableClauseDictCopy.keys() :
        if resolvents.issubset(usableClauseDictCopy[el]) :
            del(usableClauseDict[el])
    

    return True


def plResolve(pair,objects) :

    set1 = pair[0]
    set2 = pair[1]

    set1copy  = set(set1.copy())
    set2copy = set(set2.copy())

    set1positive = set()
    set1negative = set()

    set2positive = set()
    set2negative = set()

    for el in set1 :
        if el.startswith("~") :
            set1negative.add(el[1:])
        
        else :
            set1positive.add(el)

    for el in set2 :
        if el.startswith("~") :
            set2negative.add(el[1:])
        
        else :
            set2positive.add(el)

    
    for el in set1positive :
        if el in set2negative :

            set1copy.remove(el)
            set2copy.remove(str("~" + el))

            newSet = set1copy.union(set2copy)

            set1obj = None
            set2obj = None

            for elem in objects :
                if elem.literals == set1 :
                        set1obj  = elem
                
                if elem.literals == set2 :
                        set2obj = elem

            objects.add(Clause(newSet,tuple((set1obj,set2obj))))

            return  newSet

    for el in set1negative :
        if el in set2positive :

            set1copy.remove(str("~" + el))
            set2copy.remove(el)

            newSet = set1copy.union(set2copy)
            
            set1obj = None
            set2obj = None

            for elem in objects :
                if elem.literals == set1 :
                        set1obj  = elem
                
                if elem.literals == set2 :
                        set2obj = elem

            objects.add(Clause(newSet,tuple((set1obj,set2obj))))

            return newSet

    return "/"

def SoSredundancyCheck(SoS) :

    soscopy = SoS.copy()

    for el in soscopy :
        for el2 in soscopy :
            if el.issubset(el2) :
                set(SoS).remove(el2)

def NewRedundancyCheck(new) :
    newcopy = new.copy()
    for el in newcopy :
        for el2 in newcopy :
            if el.issubset(el2) :
                set(new).remove(el2)


def resolve (usableClausesDict,SoS,objects) :
    
    checked = set()

    while True :
        new = set()
        
        allPairs = set()
        
        for el in SoS :
            for el2 in usableClausesDict.values() :
                if tuple((frozenset(el2),frozenset(el))) not in checked :
                    checked.add(tuple((frozenset(el2),frozenset(el))))
                    allPairs.add(tuple((frozenset(el2),frozenset(el))))

        for el in SoS :
            for el2 in SoS :
                if el != el2 : 
                    if tuple((frozenset(el2),frozenset(el))) not in checked :
                        checked.add(tuple((frozenset(el2),frozenset(el))))
                        allPairs.add(tuple((frozenset(el2),frozenset(el))))

        #print("Pairs:",allPairs)
        SoSredundancyCheck(SoS)

        for pair in allPairs :
            
            resolvents = plResolve(pair,objects=objects)
            
            if resolvents != "/" and RedundancyCheck(resolvents= resolvents,usableClauseDict=usableClausesDict) and resolvents not in new :
                new.add(frozenset(resolvents))

                if len(resolvents) == 0 :
                    return "NIL"

            
        NewRedundancyCheck(new=new)    


        for el in new :
            if el not in SoS :
                SoS.add(frozenset(el))
        

        if len(new) == 0: 
            return "FAIL"
        
        

def printParents(clause) :


    if clause.parents[0] == None or clause.parents[1] == None :
        return "Kraj"

    else :
        printParents(clause.parents[0])
        printParents(clause.parents[1])     
    
    clause.printAttrs()



# parsing the input

parser = argparse.ArgumentParser()

parser.add_argument('action',choices=['resolution', 'cooking'])
parser.add_argument('file_dirs',nargs='+')  # will be 1 or 2 args , any more args will be ignored in code

args = parser.parse_args()


# main actions based on input 

if args.action == 'resolution' :

    clausesList = list()
    usableClausesDict = dict()
    usableClausesSet = set()
    SoS = set()
    objects = set()

    print("====== Clauses: ======")  
    print(" ")
    
    with open(args.file_dirs[0],'r') as clauses :  # args.file_dirs[0] is the path to clauses .txt file, and is the only one needed
        contents = clauses.readlines()
        
        for line in contents :
            if line.startswith("#") :        
                pass
            
            elif line == contents[-1] :
                clausesList.append(line[:-1])
                print("Target clause: ",line[:-1])
            else :
                clausesList.append(line[:-1])
                print(line[:-1])

    print(" ")
    print("=======================")
    
    target = clausesList[-1]
    clausesList.remove(target)
    split_input = target.split(' ')
    negated_split_input = ["~" + el for el in split_input if not ( el.startswith("v") or el.startswith("V"))]
    

    for el in negated_split_input :    # filling SoS with negated target clause literals
        if el.startswith("~~") :
            tempSet = set()
            tempSet.add(el[2:])
            SoS.add(frozenset(tempSet))
            objects.add(Clause(tempSet,tuple((None, None))))
            
        
        else :
            tempSet = set()
            tempSet.add(el)
            SoS.add(frozenset(tempSet))
            objects.add(Clause(tempSet,tuple((None, None))))
            

    print("SoS:")
    for el in SoS :
        print(el)
    print("=======================")
    print(" ")
    initialRedundancyCheck(clausesList=clausesList,isCooking=False)  # removing redundant clauses

    counter = 0
    clausesList  = list(dict.fromkeys(clausesList))

    for el in clausesList :
        counter = counter + 1
        tempClause = set()
        for el2 in el.split(' ') :
            if not (el2 == "v" or el2 == "V") :
                tempClause.add(el2)
        
        usableClausesDict[counter] = tempClause
        objects.add(Clause(tempClause,tuple((None,None))))

    counter2 = 0
    print(" ")
    print("===== New Clauses: =====")
    for el in clausesList :
        counter2 = counter2 + 1
        print("{}. {}".format(counter2,el))
    
    print("========================")


    result = resolve(usableClausesDict=usableClausesDict,SoS=SoS,objects=objects)
    
   
    for el in objects :
            if len(el.literals) == 0 :
                printParents(clause=el) 

    if result == "NIL" :
        
        print(" ")
        print("[CONCLUSION]: {} is true".format(target))

    if result == "FAIL" :
        print(" ")
        print("[CONCLUSION]: {} is unknown".format(target))
    



if args.action == 'cooking' :

    inputCommandsList = list()
    clausesList = list()
    
    print(" ")
    print("====== Constructed with knowledge: ======")   
    print(" ")

    with open(args.file_dirs[0],'r') as clauses :  # args.file_dirs[0] is the path to clauses .txt file
        contents = clauses.readlines()
        
        for line in contents :
            if line.startswith("#") :        
                pass
            
            else :
                clausesList.append(line[:-1])
                print(line)


    print("=========================================")
    print(" ")

    with open(args.file_dirs[1],'r') as inputs :
        input_contents = inputs.readlines()

        for inputLine in input_contents :
            if inputLine.startswith("#") :
                pass

            else :
                inputCommandsList.append(inputLine[:-1])
            

    for command in inputCommandsList :
        withoutCommChar = command[:-1].strip()
                
        if command[-1] == "+" : 
            clausesList.append(withoutCommChar)
            print("User’s command: {}".format(command))
            print("Added {} \n".format(command[:-1]))


        elif command[-1] == "-" :
            clausesList.remove(withoutCommChar)
            print("User’s command: {}".format(command))
            print("Removed {} \n".format(command[:-1]))


        elif command[-1] == "?" :
            print("User’s command: {}".format(command))
            
            usableClausesDict = dict()
            usableClausesSet = set()
            SoS = set()
            objects = set()

            
            target = command.split(' ')[0]
            split_input = target.split(' ')
            negated_split_input = ["~" + el for el in split_input if not ( el.startswith("v") or el.startswith("V"))]
            

            for el in negated_split_input :    # filling SoS with negated target clause literals
                if el.startswith("~~") :
                    tempSet = set()
                    tempSet.add(el[2:])
                    SoS.add(frozenset(tempSet))
                    objects.add(Clause(tempSet,tuple((None, None))))
                    
        
                else :
                    tempSet = set()
                    tempSet.add(el)
                    SoS.add(frozenset(tempSet))
                    objects.add(Clause(tempSet,tuple((None, None))))
                    

            initialRedundancyCheck(clausesList=clausesList,isCooking=True)  # removing redundant clauses


            counter = 0
            clausesList  = list(dict.fromkeys(clausesList))

            for el in clausesList :
                counter = counter + 1
                tempClause = set()
                for el2 in el.split(' ') :
                    if not (el2 == "v" or el2 == "V") :
                        tempClause.add(el2)
                        
        
                usableClausesDict[counter] = tempClause
                objects.add(Clause(tempClause,tuple((None,None))))


            result = resolve(usableClausesDict=usableClausesDict,SoS=SoS,objects=objects)
            

            for el in objects :
                if len(el.literals) == 0 :
                    printParents(clause=el)

            if result == "NIL" :
                
                print(" ")
                print("[CONCLUSION]: {} is true".format(target))

            if result == "FAIL" :
                
                print(" ")
                print("[CONCLUSION]: {} is unknown".format(target))

            print(" ")
            